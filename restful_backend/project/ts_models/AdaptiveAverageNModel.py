import numpy as np
from .BaseModel import BaseModel

class AdaptiveAverageNModel(BaseModel):
    def __init__(self, round_non_negative_int_func, latest_n=24):
        self.round_non_negative_int_func = round_non_negative_int_func
        self.eval_len = latest_n
        self.model_name = "Adaptive_Average_N_Model"
    
    def fit(self, data):
        if len(data) == 0:
            self.status = -2
            self.average = 0
        elif len(data) < self.eval_len+1:
            self.status = -1
            self.average = np.mean(data)
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
                    prediction = np.mean(test_ts[-n:])
                    all_prediction.append(prediction)
                    all_actual.append(real_request)
                eval_score = self.evaluation_function(pred=all_prediction, actual=all_actual)
                if eval_score > last_eval_score:
                    self.status = n
                    last_eval_score = eval_score
                else:
                    continue
            self.average = np.mean(data[-self.status:])
    
    def eval_accuracy(self, actual, pred, overestimate_cost, model_name):
        hit_count = 0
        over_estimate_count = 0
        under_estimate_count = 0
        request_count = sum(actual)
        accuracy = {}
        for i in range(len(actual)):
            hit_count = hit_count + min(actual[i], pred[i])
            if(pred[i] > actual[i]):
                over_estimate_count = over_estimate_count + pred[i] - actual[i]
            else:
                under_estimate_count = under_estimate_count + actual[i] - pred[i]

        hit_rate = (hit_count+1) / (request_count+1)
        over_estimate_rate = (over_estimate_count +1) / (request_count + 1)
        under_estimate_rate = (under_estimate_count +1) / ( request_count + 1)
        overall_score = hit_rate - overestimate_cost * over_estimate_rate + (1 if hit_rate > 0.35 else 0)

        accuracy["model_name"] = model_name
        accuracy["overall_score"] = overall_score
        accuracy["hit_rate"] = hit_rate
        accuracy["over_estimate_rate"] = over_estimate_rate
        accuracy["under_estimate_rate"] = under_estimate_rate
        accuracy["request_count"] = request_count
        accuracy["hit_count"] = hit_count
        accuracy["over_estimate_count"] = over_estimate_count
        accuracy["under_estimate_count"] = under_estimate_count
        accuracy["prediction"] = pred
        
        return accuracy
        
    
    def predict(self, next_n_prediction):
        return self.round_non_negative_int_func([self.average] * next_n_prediction)


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
