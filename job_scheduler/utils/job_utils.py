import settings
import os


def get_job_workdir_from_id(job_id):
    return os.path.join(settings.DATA_DIR, str(job_id))

def get_job_name_from_id(job_id):
    return 'trainer' + f'_{job_id}'

def get_job_volume_from_id(job_id):
    return 'vol' + f'_{job_id}'
