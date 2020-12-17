from .BaseModel import BaseModel
import xgboost as xgb

class XGBoostModel(BaseModel):
    def __init__(self, metric, **kwargs):
        self.model = xgb.XGBRegressor(objective=metric, **kwargs)
        self.features = True

    def fit(self, x, y):
        self.model.fit(x, y, verbose=False)
    
    def predict(self, x):
        return self.model.predict(x)

    def save(self, path):
        self.model.save_model(path)
        return path

