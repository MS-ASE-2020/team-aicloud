import rpyc
from job_manager import JobManager
import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from common.session import session_scope


class SchedulerService(rpyc.Service):
    def __init__(self):
        self.manager = JobManager()
        self.base = automap_base()
        self.engine = create_engine(settings.CONNECTION_STR)
        self.base.prepare(self.engine, reflect=True)
        self.Session = sessionmaker(bind=self.engine)

    def exposed_push(self, job_id):
        Job = self.base.classes.project_job
        print('here')
        with session_scope(self.Session) as session:
            print('before query')
            job = session.query(Job).get(job_id)
            print('after query')
            for series in job.project_series_collection:
                print(series.id)
                self.manager.push(series.id)

    def exposed_cancel(self, job_id):
        self.manager.cancel(job_id)
