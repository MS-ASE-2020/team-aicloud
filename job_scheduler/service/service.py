import rpyc
from scheduler.job_manager import JobManager
import json
import os
from utils.job_utils import get_job_workdir_from_id, get_job_name_from_id


class SchedulerService(rpyc.Service):
    def __init__(self):
        self.manager = JobManager()

    def exposed_get_status_or_result(self, job_id):
        return self.manager.get_job_status(job_id)

    def exposed_push(self, data, job, series, model):
        job_id = job['id']
        config_json = {
            'data': data,
            'job': job,
            'series': series,
            'model': model,
        }

        work_dir = get_job_workdir_from_id(job_id)
        config_path = os.path.join(work_dir, 'config.json')
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_json, f, indent=4)

        self.manager.create_job(job_id, work_dir)

    def exposed_cancel(self, job_id):
        self.manager.delete_job(job_id)
