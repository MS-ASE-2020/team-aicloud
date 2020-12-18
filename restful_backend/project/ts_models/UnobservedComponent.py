import statsmodels.api as sm
from .BaseModel import BaseModel

class UnobservedComponentModel(BaseModel):
    def __init__(self, round_non_negative_int_func):
        self.model_name = "UnobservedComponentModel"
        self.round_non_negative_int_func = round_non_negative_int_func

    def fit(self, ts):
        unrestricted_model = {
            'level': 'local linear trend', 'cycle': False #, 'seasonal': 24 * 7
        }

        model = sm.tsa.UnobservedComponents(endog=ts, **unrestricted_model)
        self.trained_model = model.fit()
        return self

    def predict(self, next_n):
        prediction = self.trained_model.forecast(steps=int(next_n))
        return self.round_non_negative_int_func(prediction)
