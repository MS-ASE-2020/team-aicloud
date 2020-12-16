import settings
from utils.rediswq import RedisWQ


class JobManager:
    def __init__(self):
        self._q = RedisWQ(name=settings.QUEUE, host=settings.REDIS_HOST)

    def push(self, job_id):
        self._q.push(job_id)

    def get_status(self, job_id):
        return self._q.status(job_id)

    def cancel(self, job_id):
        self._q.delete(job_id)
