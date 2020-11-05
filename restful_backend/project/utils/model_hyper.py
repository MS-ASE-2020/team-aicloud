import json
import os
import numpy as np
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

def _adaptive_average_hyper(latest_n=5):
    hyper = dict()
    hyper['latest_n'] = latest_n
    return hyper

def _adaptive_maxn_hyper(latest_n=5):
    hyper = dict()
    hyper['latest_n'] = latest_n
    return hyper

def _arima_hyper(latest_n=5):
    hyper = dict()
    hyper['latest_n'] = latest_n
    return hyper

def _prophet_hyper(changepoint_prior_scale=0.1, add_std_factor=0.1):
    hyper = dict()
    hyper['changepoint_prior_scale'] = changepoint_prior_scale
    hyper['add_std_factor'] = add_std_factor    
    return hyper

def _linear_fit_hyper(add_std_factor=0.1, latest_n=5):
    hyper = dict()
    hyper['latest_n'] = latest_n
    hyper['add_std_factor'] = add_std_factor
    return hyper

def _lstm_hyper(lstm_cells_per_layer_used=100, sample_num=5):
    hyper = dict()
    hyper['lstm_cells_per_layer_used'] = lstm_cells_per_layer_used
    hyper['sample_num'] = sample_num
    return hyper

def _lstm_long_hyper(lstm_cells_per_layer_used=100, sample_num=5, loss_used=['mean_squared_error']):
    hyper = dict()
    hyper['lstm_cells_per_layer_used'] = lstm_cells_per_layer_used
    hyper['loss_used'] = loss_used
    hyper['sample_num'] = sample_num
    return hyper

def _new_random_arrival_hyper(
    spike_detect_lag=12,
    spike_detect_std_threshold=2,
    spike_detect_influence=0.5,
    latest_n=5,
    rise_strategy=["exponential", "expectation", "linear", "auto"],
    decline_strategy=["exponential", "expectation", "linear"],
    confidence_threshold=0.5,
    height_limit=["average", "max_n"]
):
    hyper=dict()
    hyper['spike_detect_lag'] = spike_detect_lag
    hyper['spike_detect_std_threshold'] = spike_detect_std_threshold
    hyper['spike_detect_influence'] = spike_detect_influence
    hyper['latest_n'] = latest_n
    hyper['rise_strategy'] = rise_strategy
    hyper['decline_strategy'] = decline_strategy
    hyper['confidence_threshold'] = confidence_threshold
    hyper['height_limit'] = height_limit
    return hyper

def _random_arrival_hyper(fit_model=[ "Expon", "Weibull", "Sampling"]):
    hyper = dict()
    hyper['fit_model'] = fit_model
    return hyper

# generate mdoel hyper-parameaters
MODELS = {
    'AdaptiveAverage': _adaptive_average_hyper,
    'AdaptiveMaxN': _adaptive_maxn_hyper,
    'ARIMA': _arima_hyper,
    'Prophet': _prophet_hyper,
    'LinearFit': _linear_fit_hyper,
    'LSTM': _lstm_hyper,
    'LSTMLong': _lstm_long_hyper,
    'NewRandomArrival': _new_random_arrival_hyper,
    'RandomArrival': _random_arrival_hyper
}

def generate_hyper(path='model_hypers.json'):
    hypers = {}
    for name, model_name in MODELS.items():
        model_hyper = MODELS[name]()
        hypers[name] = model_hyper

    with open(path, 'w') as f:
        json.dump(hypers, f)
    return hypers

def get_models():
    models = []
    for name in MODELS.keys():
        models.append(name)
    
    return models

def get_model_hyper(model_name):
    model_hypers = []
    if model_name in MODELS.keys():
        hypers = MODELS[model_name]()
        for key, val in hypers.items():
            model_hyper = dict()
            model_hyper["label"] = key
            # TODO: add model hyper intro
            model_hyper["intro"] = "hyper-parameters description"
            model_hyper["val"] = val
            model_hypers.append(model_hyper)
        return model_hypers
    else:
        raise Exception("unexpected model name %s" %model_name)

def set_model_hyper(model_name, **kwargs):
    if model_name.lower() in MODELS.keys():
        MODELS[model_name](**kwargs)
        # TODO: save it to json or database config
        return MODELS[model_name]()
    else:
        raise Exception("unexpected model name %s" %model_name)
    
def hyper_space(model, udf_parameter=None, path='utils/model_hypers.json'):
    # use default configuration
    space = {}
    if udf_parameter is None:
        if not os.path.exists(path):
            generate_hyper(path)
            print('generate hyperparameters json')
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

def getBestModelfromTrials(trials):
    valid_trial_list = [trial for trial in trials
                            if STATUS_OK == trial['result']['status']]
    losses = [ float(trial['result']['loss']) for trial in valid_trial_list]
    index_having_minumum_loss = np.argmin(losses)
    best_trial_obj = valid_trial_list[index_having_minumum_loss]
    return best_trial_obj['result']['trained_Model'], np.min(losses)

if __name__ == '__main__':
    hypers = generate_hyper()
    print(get_model())
    print(get_model_hyper('AdaptiveMaxN'))

    