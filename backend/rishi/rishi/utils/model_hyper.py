import json

def _adaptive_average_hyper(latest_n=5):
    hyper = dict()
    hyper['latest_n'] = latest_n
    return hyper

def _adaptive_maxn_hyper(latest_n=5):
    hyper = dict()
    hyper['latest_n'] = latest_n
    return hyper

def _adrima_hyper(latest_n=5):
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
    'adaptiveaverage': _adaptive_average_hyper,
    'adaptivemaxn': _adaptive_maxn_hyper,
    'adrima': _adrima_hyper,
    'prophet': _prophet_hyper,
    'linearfit': _linear_fit_hyper,
    'lstm': _lstm_hyper,
    'lstmlong': _lstm_long_hyper,
    'newrandomarrival': _new_random_arrival_hyper,
    'randomarrival': _random_arrival_hyper
}

def generate_hyper(path='model_hypers.json'):
    hypers = {}
    for name, model_name in MODELS.items():
        model_hyper = MODELS[name]()
        hypers[name] = model_hyper

    with open(path, 'w') as f:
        json.dump(hypers, f)
    
    return hypers

def get_model_hyper(model_name):
    if model_name in MODELS.keys():
        hypers = MODELS[model_name]()
        return hypers
    else:
        raise Exception("unexpected model name %s" %model_name)

def set_model_hyper(model_name, **kwargs):
    if model_name.lower() in MODELS.keys():
        MODELS[model_name](**kwargs)
        # TODO: save it to json or database config
        return MODELS[model_name]()
    else:
        raise Exception("unexpected model name %s" %model_name)
    

if __name__ == '__main__':
    hypers = generate_hyper()
    print(hypers)
    print(get_model_hyper('AdaptiveMaxN'))

    