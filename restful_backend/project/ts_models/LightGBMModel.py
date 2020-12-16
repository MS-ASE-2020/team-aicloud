import lightgbm as lgb
from .BaseModel import BaseModel

class LightGBMModel(BaseModel):
    def __init__(self, **kwargs):
        self.model = lgb.LightGBMRegressor(**kwargs)

    def fit(self, x, y):
        self.model.fit(x, y)

    def predict(self, x):
        self.model.predict(x)

    def save(self, path):
        self.save_model(path)