import pickle
import os

class BaseModel:
    def __init__(self, features=False):
        self.features = features
        self.model_save = False

    def fit(self):
        raise NotImplementedError

    def predict(self):
        raise NotImplementedError

    def save(self, path):
        if self.model_save:
            print('Saving model...')
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + '/model.pkl', 'wb') as fd:
                pickle.dump(self.model, fd)
            return path

        # Models without parameters
        return None

    def __repr__(self):
        if not hasattr(self, 'description'):
            self.description = 'A time series prediction model'
        return 'Class: %s \n Description: %s'.format(self.__class__.__str__, self.description)