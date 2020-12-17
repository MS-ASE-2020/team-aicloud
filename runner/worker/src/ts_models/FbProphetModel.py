import pandas as pd
from fbprophet import Prophet
from .BaseModel import BaseModel
import datetime

class FbProphetModel(BaseModel):

    def __init__(self, round_non_negative_int_func, add_std_factor = 0.25, changepoint_prior_scale=0.3):
        self.model_name = "FbProphetModel"
        self.round_non_negative_int_func = round_non_negative_int_func
        self.changepoint_prior_scale = changepoint_prior_scale
        self.add_std_factor = add_std_factor
        self.model = None
        self.model_save = True
    
    # FIXME: ts + data?
    def fit(self, data):
        # add fake timestamp for prediction
        start_ts = datetime.datetime.strptime("2010-01-01", "%Y-%m-%d")
        interval = datetime.timedelta(days=1)
        ts = [datetime.datetime.strftime(start_ts + (i + 1) * interval, "%Y-%m-%d %X") for i in range(len(data))]
        _dic = {'ds': ts, 'y': data}
        _df = pd.DataFrame(data=_dic)
        self.model = Prophet(changepoint_prior_scale = self.changepoint_prior_scale).fit(_df)
        return self

    def predict(self, next_n_prediction, past_n_validation=5):
        _past_and_future = self.model.make_future_dataframe(periods=next_n_prediction, freq='H')
        _forecast = self.model.predict(_past_and_future)
        _recent_future_pred = _forecast.tail(next_n_prediction + past_n_validation)

        _recent_future_pred_array = _recent_future_pred["yhat"] + self.add_std_factor * (_recent_future_pred["yhat_upper"] - _recent_future_pred["yhat"])
        _recent_future_pred_array = self.round_non_negative_int_func(_recent_future_pred_array)

        _validate_pred = _recent_future_pred_array[0:past_n_validation]
        _future_pred = _recent_future_pred_array[-next_n_prediction:]
        # print('future_pred: ', _future_pred)
        # print('val_pred: ', _validate_pred)
        return _future_pred
