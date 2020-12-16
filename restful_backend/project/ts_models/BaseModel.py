import pickle

class BaseModel:
    def __init__(self, features=False):
        self.features = features

    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def save(self, path):
        with open(path, 'wb') as fd:
            pickle.dump(self.model, path)

    def __repr__(self):
        if not hasattr(self, description):
            self.description = 'A time series prediction model'
        return 'Class: %s \n Description: %s'.format(self.__class__.__str__, self.description)