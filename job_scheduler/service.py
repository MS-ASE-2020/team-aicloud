import rpyc


class SchedulerService(rpyc.Service):
    def exposed_get_status_or_result(job_id):
        pass

    def exposed_push(job):
        pass

    def exposed_cancel(job_id):
        pass
