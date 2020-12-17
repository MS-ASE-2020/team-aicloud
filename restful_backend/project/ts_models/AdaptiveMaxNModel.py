import numpy as np
from .BaseModel import BaseModel

class AdaptiveMaxNModel(BaseModel):
    def __init__(self, round_non_negative_int_func, latest_n=24):
        super(AdaptiveMaxNModel, self).__init__()
        self.round_non_negative_int_func = round_non_negative_int_func
        self.eval_len = latest_n
        self.model_name = "Adaptive_Max_N_Model"

    def fit(self, data):
        if len(data) == 0:
            self.status = -2
            self.max = 0
        elif len(data) < self.eval_len+1:
            self.status = -1
            self.max = np.max(data)
        else:
            eval_len = min(len(data)//2, self.eval_len)
            last_eval_score = -np.inf
            for n in range(1, eval_len+1):
                eval_ts = self._split_ts(data, self.eval_len, n)
                all_prediction = []
                all_actual = []
                for ts in eval_ts:
                    test_ts = ts[:-1]
                    real_request = ts[-1]
                    prediction = np.max(test_ts[-n:])
                    all_prediction.append(prediction)
                    all_actual.append(real_request)
                eval_score = self.evaluation_function(
                    pred=all_prediction, actual=all_actual)
                if eval_score > last_eval_score:
                    self.status = n
                    last_eval_score = eval_score
                else:
                    continue
            self.max = np.max(data[-self.status:])

    def predict(self, next_n_prediction):
        return [self.max] * next_n_prediction

    def _split_ts(self, data, eval_len, n):
        ts_list = [data[-(n+1):]]
        for i in range(1, eval_len):
            sub_ts = data[-(i+n+1): -i]
            ts_list.append(sub_ts)
        return ts_list

    def evaluation_function(self, actual, pred):
        """ Mean Squared Error """
        actual = np.array(actual)
        pred = np.array(pred)
        return np.mean(np.square(actual - pred))
