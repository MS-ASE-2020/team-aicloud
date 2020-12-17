import json
import os
from hyperopt import hp
from .model_hyper import generate_hyper


if __name__ == '__main__':
    MODELS = [
        'adaptiveaveragen',
        'adaptivemaxn',
        'adrima',
        'prophet',
        'linearfit',
        'lstm',
        'lstmlong',
        'newrandomarrival',
        'randomarrival' 
    ]
    for name in MODELS:
        space = hyper_space(name)
        print(space)
    