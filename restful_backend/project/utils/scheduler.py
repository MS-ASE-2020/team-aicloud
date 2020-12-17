import rpyc
from django.conf import settings


def commit_job(job_id):
    conn = rpyc.connect(settings.SCHEDULER_HOST, settings.SCHEDULER_PORT)
    conn.root.push(job_id)

