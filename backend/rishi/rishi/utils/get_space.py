import json
from hyperopt import hp
from model_hyper import generate_hyper

def hyper_space(model, udf_parameter=None, path='model_hypers.json'):
    # use default configuration
    space = {}
    if udf_parameter is None:
        if not exit(path):
            generate_hyper()
        with open(path) as f:
            parameters = json.load(f)[model]
        # parameters = {name: [type, default_name if int or double else enum_list]}
        hp_type = {"int": "uniformint", "float": "uniform", "list": "choice"}
        for name, val in parameters.items():
            if isinstance(val, int) or isinstance(val, float):
                space[name] = getattr(hp, hp_type[type(val).__name__])(name, 0, 10*val)
            elif isinstance(val, list):
                space[name] = getattr(hp, hp_type[type(val).__name__])(name, val)
            else:
                raise Exception("Unexpected type: %s parameter %s in Model %s is not supported" % (val, type(val), name, model))
    else:
        pass
    return space



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
    