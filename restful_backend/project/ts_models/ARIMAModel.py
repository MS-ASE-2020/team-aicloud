from statsmodels.tsa.arima_model import ARIMA
from .BaseModel import BaseModel

# FIXME: how to pass arima_order
class ARIMAModel(BaseModel):
    def __init__(self, round_non_negative_int_func, add_std_factor=0):
        # FIXME: fix arima_order type
        super.__init__()
        self.arima_order = (6, 0, 2)
        self.add_std_factor = add_std_factor
        self.model_name = "ARIMA_{}_Model".format(self.arima_order)
        self.model_save = True

    def fit(self, data):
        model = ARIMA(data, order=self.arima_order)
        self.model_fit = model.fit(disp=0)
        return self

    def predict(self, next_n_prediction):
        pred, stderr, cof_int = self.model_fit.forecast(steps=next_n_prediction)
        pred_std = pred + self.add_std_factor * stderr
        return pred_std
    
