import json
from metrics import *
import ts_models
import datetime
import pandas as pd


def get_validation_period(ts_data):
    """
    Evaluate how long should be the validation data set
    @param ts_data: the time series data
    @return: an integer represents the last k points for validation
    """
    total_sum = sum(ts_data)
    total_points = len(ts_data)
    per_point_sum = total_sum / total_points
    min_points = 5
    max_points = 48
    tolerance = 0.8
    vpts = 0
    # limit the validation points to be at least 5 data points and at most 48 data points
    if total_points <= min_points:
        return min_points

    cumSum = sum(ts_data[-min_points+1:])
    for i in range(min_points, min(max_points, total_points)):
        vpts = i
        cumSum += ts_data[-i]
        threshold = per_point_sum * i * tolerance
        if cumSum >= threshold:
            break

    return vpts


def round_non_negative_int(arr):
    return [round(p) if p > 0 else 0 for p in arr]


class trainer():
    def __init__(self, model_name, config, eval_lastest_n=5, metrics=("mse", "rmse")):
        self.config = config
        self.metrics = metrics
        self.model_name = model_name
        self.model = None
        self.eval_lastest_n = eval_lastest_n

    def preprocess(self, ts_data, ts, features):
        self.start_ts = min(ts)
        self.interval = 1
        self.end_ts = max(ts)
        return ts_data

    def train(self, data_df, auto_tune=False):
        ts_data_array = data_df["TimeSeriesValues"].to_numpy()
        ts = data_df["TimeSeries"].to_numpy()
        if "Features" in data_df.columns:
            features = data_df["Features"].to_numpy()
        else:
            features = None
        non_zero_data = self.preprocess(ts_data_array, ts, features)
        # train test split
        # TODO: support multi-features
        recent_n_validation = get_validation_period(non_zero_data)
        if len(non_zero_data) > recent_n_validation:
            short_term_train_data = non_zero_data[0:-recent_n_validation]
            short_term_validation_data = non_zero_data[-recent_n_validation:]
        else:
            short_term_train_data = non_zero_data
            short_term_validation_data = non_zero_data + \
                [0] * (recent_n_validation - len(non_zero_data))

        self.model = getattr(ts_models, self.model_name)(
            round_non_negative_int_func=round_non_negative_int,
            **self.config)
        self.model.fit(short_term_train_data)
        pred = self.model.predict(self.eval_lastest_n)
        results = dict()
        for name in self.metrics:
            results[name] = METRICS[name](short_term_validation_data, pred)

        return results

    def save(self, path):
        pass

    def predict(self, nextKPrediction):
        pred = self.model.predict(nextKPrediction)
        
        predictions = dict()
        for i in range(nextKPrediction):
            # FIXME: only support day
            predictions[datetime.datetime.strptime(self.end_ts, "%Y-%M-%d") +
                        datetime.timedelta(days=(i + 1) * self.interval)] = pred[i]

        return predictions


if __name__ == '__main__':
    config = {
        "latest_n": 5,
        "add_std_factor": 0.5
    }
    model_name = "LinearFitModel"
    path = 'foo.csv'
    df = pd.read_csv(path)
    trainer = trainer(model_name, config)
    results = trainer.train(df)
    pred = trainer.predict(5)
    print(results)
    # {'mse': 1826699.0, 'rmse': 1351.5542904374947}
    print(pred)
    # {datetime.datetime(2020, 1, 8, 0, 9): 1254, datetime.datetime(2020, 1, 9, 0, 9): 1251, ...
