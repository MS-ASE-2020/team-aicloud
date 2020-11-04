import json
import os
from metrics import *
import ts_models
import datetime
import pandas as pd
import utils
import hyperopt
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

class trainer():
    def __init__(self, model_name, config, auto_tune=True, metrics=("mse", "rmse"), max_eval=100):
        self.config = config
        self.metrics = metrics
        self.model_name = model_name
        self.model = None
        self.auto_tune = auto_tune
        self.features = False
        self.max_eval = max_eval

    def preprocess(self, ts_data, ts, features):
        self.start_ts = datetime.datetime.strptime(min(ts), "%Y-%m-%d")
        self.end_ts = datetime.datetime.strptime(max(ts), "%Y-%m-%d")
        self.interval = (self.end_ts - self.start_ts) / (len(ts) - 1)
        if features is None:
            features = ts_data
        return features, ts_data

    def train(self, data_df):
        ts_data_array = data_df["TimeSeriesValues"].to_numpy()
        ts = data_df["TimeSeries"].to_numpy()
        if "Features" in data_df.columns:
            features = data_df["Features"].to_numpy()
            self.features = True
        else:
            features = None
        X, y = self.preprocess(ts_data_array, ts, features)
        # train test split
        # TODO: split into train val test 
        self.recent_n_validation = utils.get_validation_period(X)
        if len(X) > self.recent_n_validation:
            self.X_train = X[0:-self.recent_n_validation]
            self.y_train = y[0:-self.recent_n_validation]
            self.X_valid = X[-self.recent_n_validation]
            self.y_valid = y[-self.recent_n_validation]
        else:
            self.X_train = X
            self.y_train = y
            self.X_valid = X + [0] * (self.recent_n_validation - len(X))
            self.y_valid = y + [0] * (self.recent_n_validation - len(y))

        if not self.auto_tune:
            self.model = self._train(config)["trained_Model"]
            best = self.config
        else:
            space = utils.hyper_space(self.model_name.lower())
            trials = Trials()
            best = fmin(fn=self._train,
                        space=space,
                        algo=tpe.suggest,
                        max_evals=self.max_eval, 
                        trials=trials)
            print(best)
            tuned_model, min_loss = utils.getBestModelfromTrials(trials)
            self.model = tuned_model
        
        pred = self._predict(self.recent_n_validation)
        results = self._eval(pred, self.y_valid)
        results["config"] = best 

        return results

    def predict(self, nextKPrediction):
        pred = self._predict(nextKPrediction) 
        
        predictions = dict()
        for i in range(nextKPrediction):
            ts = self.end_ts + (i + 1) * self.interval
            ts = datetime.datetime.strftime(ts, "%Y-%m-%d %X")
            predictions[ts] = pred[i]

        return predictions

    # save model 
    def save(self, path):
        pass

    def _train(self, space):
        model = getattr(ts_models, self.model_name)(
            round_non_negative_int_func=utils.round_non_negative_int,
            **space)

        if self.features:
            model.fit(self.X_train, self.y_train)
            pred = self.model.predict(self.X_train, self.recent_n_validation)
        else:
            model.fit(self.y_train)
            pred = model.predict(self.recent_n_validation)

        # if auto-tune, only use mse as metrics
        if self.auto_tune:
            loss = METRICS["mse"](self.y_valid, pred)
            return {'loss': loss, 'status': STATUS_OK, 'trained_Model': model}
        else:
            return {'trained_Model': model}  
    
    def _eval(self, pred, truth):
        results = dict()
        for name in self.metrics:
            results[name] = METRICS[name](self.y_valid, pred)

        return results
    
    def _predict(self, nextKPrediction):
        pred = self.model.predict(nextKPrediction) if not self.features else self.model.predict(self.X_valid, nextKPrediction)
        return pred

if __name__ == '__main__':
    config = {
        "latest_n": 5,
        "add_std_factor": 0.5
    }
    model_name = "LinearFitModel"
    path = '/home/yaq/team-aicloud/restful_backend/uploads/foo.csv'
    df = pd.read_csv(path)
    trainer = trainer(model_name, config)
    results = trainer.train(df)
    pred = trainer.predict(5)
    print(results)
    # {'mse': 1826699.0, 'rmse': 1351.5542904374947}
    print(pred)
    # {datetime.datetime(2020, 1, 8, 0, 9): 1254, datetime.datetime(2020, 1, 9, 0, 9): 1251, ...
