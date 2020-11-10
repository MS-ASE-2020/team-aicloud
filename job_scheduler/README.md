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