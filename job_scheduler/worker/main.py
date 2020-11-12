import argparse
from utils import dataset_utils
import json
import os
from . import trainer


def train(dataset_path, groupby_indexs, groupby_val, model_name, hyper_param, target_idx, ts_idx, feature_idx, nextKprediction):
    dataset = dataset_utils.get_sliced_dataset(dataset_path, groupby_indexs, groupby_val)
    model = trainer.trainer(model_name, hyper_param)
    metrics, config, tuned_model = model.train(dataset, target_idx, ts_idx, feature_idx)
    pred = model.predict(nextKprediction)
    model_file = {
        'predictions': pred,
        'metrics': metrics,
        'config': config, #hyper_params
        'model': tuned_model
    }


def main():
    work_dir = '/data'
    with open(os.path.join(work_dir, 'config.json'), 'r', encoding='utf-8') as f:
        config_json = json.load(f)
    # TODO: load config

if __name__ == '__main__':
    main()
