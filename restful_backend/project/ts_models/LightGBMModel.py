import lightgbm as lgb
from .BaseModel import BaseModel

class LightGBMModel(BaseModel):
    def __init__(self, num_round=100, **kwargs):
        super.__init__(features=True)
        if ('round_non_negative_int_func' in kwargs):
            kwargs.pop('round_non_negative_int_func')
        self.parmas = kwargs
        self.num_round = num_round

    def fit(self, x, y):
        train_data = lgb.Dataset(x, label=y)
        self.model = lgb.train(self.parmas, train_data, self.num_round)

    def predict(self, x):
        return self.model.predict(x, num_iteration=self.model.best_iteration)

    @property
    def features(self):
        return true

    def save(self, path):
        self.model.save_model(path)
        return path
