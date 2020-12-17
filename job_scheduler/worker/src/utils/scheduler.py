import rpyc

def commit_job(job_id):
    conn = rpyc.connect(hostname, port)
    conn.root.exposed_push(job_id)
