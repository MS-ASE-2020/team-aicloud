此应用使用 [RPyC](https://rpyc.readthedocs.io/en/latest) 提供接口，client-side 的使用方式为:

```python
import rpyc
conn = rpyc.connect(hostname, port)
conn.root.get_status(job_id)
```

提供以下接口：

```python
import rpyc


class SchedulerService(rpyc.Service):
    def exposed_get_status_or_result(job_id):
        pass

    def exposed_push(job):
        pass

    def exposed_cancel(job_id):
        pass
```

- `get_status_or_result`
  - `job_id`: 字符串，任务的 id
  - 返回字符串，为对应的状态。若任务完成，返回结果。
- `push`
  - ???
  - ???
- `cancel`
  - `job_id`: 字符串，任务的 id
  - 无返回值，取消该任务


## Trainer
input:
dataset_path: string
groupby_indexs: list of int
groupby_val: string
target_idx: int
ts_idx: int
feature_indexs: int
model_name: string
hyper_param: dict
nextKprediction: int

```python
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
print(pred)
print(metrics)
print(config)
# predictions: {'2020-09-08 00:00:00': 236, '2020-09-09 00:00:00': 238, '2020-09-10 00:00:00': 240, '2020-09-11 00:00:00': 242, '2020-09-12 00:00:00': 244}
# metrics: {'mse': 255.0, 'rmse': 15.968719422671311}
# config: {'latest_n': 5, 'add_std_factor': 0}
```

