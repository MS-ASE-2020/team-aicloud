import rpyc
from scheduler.job_manager import JobManager
import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


class SchedulerService(rpyc.Service):
    def __init__(self):
        self.manager = JobManager()
        self.base = automap_base()
        self.engine = create_engine(settings.CONNECTION_STR)
        self.base.prepare(self.engine, reflect=True)

    def exposed_push(self, job_id):
        Job = self.base.project_job
        with Session(self.engine) as session:
            job = session.query(Job).get(job_id)
            for series in job.project_series_collection:
                self.manager.push(series.id)

    def exposed_cancel(self, job_id):
        self.manager.cancel(job_id)
