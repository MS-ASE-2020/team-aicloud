from service import SchedulerService
import settings
from rpyc.utils.server import ThreadedServer


if __name__ == '__main__':
    server = ThreadedServer(SchedulerService, port=settings.PORT)
    server.start()
