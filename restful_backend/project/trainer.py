from .ts_models import *
import datetime
import pandas as pd
# import utils
from .utils import *
# from utils import model_hyper, eval_func
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from .utils.metrics import METRICS


class trainer:
    def __init__(self, model_name, config, auto_tune=False, metrics=("mse", "rmse"), max_eval=100, auto_tune_metric="mse"):
        self.config = config
        self.metrics = metrics
        self.model_name = model_name
        self.model = None
        self.auto_tune = auto_tune
        self.features = False
        self.max_eval = max_eval
        self.auto_tune_metric = auto_tune_metric

    def preprocess(self, ts_data, target_idx, ts_idx, feature_idx):
        # FIXME: data type is object currently
        ts = ts_data[:, ts_idx]
        self.start_ts = datetime.datetime.strptime(min(ts), "%m/%d/%Y")
        self.end_ts = datetime.datetime.strptime(max(ts), "%m/%d/%Y")
        self.interval = (self.end_ts - self.start_ts) / (len(ts) - 1)
        # directly taking related idx would result in empty dataframe
        if len(feature_idx) == 0:
            features = range(ts_data.shape[0])
        else:
            self.features = True
            features = ts_data[:, feature_idx].astype('float64')
        y = ts_data[:, target_idx].astype('float64')
        return features, y

    def train(self, data_df, target_idx, ts_idx, feature_idx):
        # TODO: test features dataset
        data = data_df.to_numpy()
        X, y = self.preprocess(data, target_idx, ts_idx, feature_idx)
        # train test split
        # TODO: split into train val test
        self.recent_n_validation = eval_func.get_validation_period(X)
        if len(X) > self.recent_n_validation:
            self.X_train = X[0:-self.recent_n_validation]
            self.y_train = y[0:-self.recent_n_validation]
            self.X_valid = X[-self.recent_n_validation:]
            self.y_valid = y[-self.recent_n_validation:]
        else:
            self.X_train = X
            self.y_train = y
            self.X_valid = X + [0] * (self.recent_n_validation - len(X))
            self.y_valid = y + [0] * (self.recent_n_validation - len(y))

        space = model_hyper.hyper_space(
            self.model_name, udf_parameter=self.config, auto_tune=self.auto_tune)
        if not self.auto_tune:
            self.model = self._train(space)["trained_Model"]
            best = self.config
        else:
            trials = Trials()
            best = fmin(fn=self._train,
                        space=space,
                        algo=tpe.suggest,
                        max_evals=self.max_eval,
                        trials=trials)
            print(best)
            self.model, min_loss = model_hyper.getBestModelfromTrials(trials)

        pred = self._predict(self.recent_n_validation)
        metrics = self._eval(pred, self.y_valid)

        return metrics, best, self.model

    def predict(self, nextKPrediction):
        pred = self._predict(nextKPrediction)

        timestamps = list()
        predictions = list()
        for i in range(nextKPrediction):
            ts = self.end_ts + (i + 1) * self.interval
            ts = datetime.datetime.strftime(ts, "%Y-%m-%d %X")
            timestamps.append(ts)
            predictions.append(pred[i])

        return predictions, timestamps

    # save model
    def save(self, path):
        self.model.save(path)

    def _train(self, space):
        model = getattr(ts_models, self.model_name + 'Model')(
            round_non_negative_int_func=eval_func.round_non_negative_int,
            **space)

        if self.features:
            model.fit(self.X_train, self.y_train)
            pred = self.model.predict(self.X_train, self.recent_n_validation)
        else:
            model.fit(self.y_train)
            pred = model.predict(self.recent_n_validation)

        # if auto-tune, only use mse as metrics
        if self.auto_tune:
            loss = METRICS[self.auto_tune_metric](self.y_valid, pred)
            return {'loss': loss, 'status': STATUS_OK, 'trained_Model': model}
        else:
            return {'trained_Model': model}

    def _eval(self, pred, truth):
        results = dict()
        for name in self.metrics:
            results[name] = METRICS[name](self.y_valid, pred)

        return results

    def _predict(self, nextKPrediction):
        pred = self.model.predict(nextKPrediction) if not self.features else self.model.predict(
            self.X_valid, nextKPrediction)
        return pred


if __name__ == '__main__':
    config = [
        {"name": "add_std_factor",
         "intro": "hyper-parameters description",
         "type": "float",
         "val": 0.1
         },
        # {
        #     "name": "loss_used",
        #     "intro": "hyper-parameters description",
        #     "type": "list",
        #     "choice": [
        #         "mean_squared_error"
        #     ]
        # },
        # # {
        # #     "name": "sample_fold_used",
        # #     "intro": "hyper-parameters description",
        # #     "type": "int",
        # #     "low": 2,
        # #     "high": 8
        # # },
        # {
        #     "name": "epochs_used",
        #     "intro": "hyper-parameters description",
        #     "type": "int",
        #     "low": 100,
        #     "high": 150
        # },
        # {
        #     "name": "batch_size_used",
        #     "intro": "hyper-parameters description",
        #     "type": "int",
        #     "low": 5,
        #     "high": 10
        # }
    ]
    model_name = "ARIMA"
    path = '../uploads/Book1.csv'
    df = pd.read_csv(path)
    trainer = trainer(model_name, config, auto_tune=True, max_eval=1)
    results = trainer.train(df, 1, 0, [])
    pred = trainer.predict(5)
    # FIXME: path: <UserID><ModelID>
    path = trainer.save('save_models/lstm/')
    print(results)
    # {'mse': 1826699.0, 'rmse': 1351.5542904374947}
    print(pred)
    # {datetime.datetime(2020, 1, 8, 0, 9): 1254, datetime.datetime(2020, 1, 9, 0, 9): 1251, ...
