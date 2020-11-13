from kubernetes import client, config
import settings
from utils.job_utils import get_job_name_from_id, get_job_volume_from_id


class JobManager:
    def __init__(self):
        config.load_kube_config()
        self.api_instance = client.BatchV1Api()
        self.load_settings()

    def load_settings(self):
        self.namespace = settings.K8S_NAMESPACE
        self.image = settings.IMAGE_NAME

    def _create_volume_mount_for_job(self, job_id, work_dir):
        source = client.V1HostPathVolumeSource(work_dir, 'Directory')
        volume_name = get_job_volume_from_id(job_id)
        client.V1Volume(host_path=source, name=volume_name)
        mount = client.V1VolumeMount('/data', name=volume_name)
        return mount

    def create_job(self, job_id, work_dir):
        name = get_job_name_from_id(job_id)
        mount = self._create_volume_mount_for_job(job_id, work_dir)
        container = client.V1Container(
            name=name,
            image=self.image,
            command=['python', 'main.py'],
            volume_mounts=[mount]
        )
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "pi"}),
            spec=client.V1PodSpec(restart_policy="Never", containers=[container])
        )
        spec = client.V1JobSpec(
            template=template,
            backoff_limit=4
        )
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_id),
            spec=spec
        )
        self.api_instance.create_namespaced_job(
            body=job,
            namespace=self.namespace
        )

    def delete_job(self, job_id):
        name = get_job_name_from_id(job_id)
        self.api_instance.delete_namespaced_job(
            name=name,
            namespace=self.namespace,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5
            )
        )

    def get_job_status(self, job_id):
        name = get_job_name_from_id(job_id)
        job = self.api_instance.read_namespaced_job_status(
            name=name,
            namespace=self.namespace
        )

        if job.status.active >= 1:
            return 'running'
        elif job.status.succeeded >= 1:
            return 'succeeded'
        elif job.status.failed >= 1:
            return 'failed'
        else:
            return 'pending'
