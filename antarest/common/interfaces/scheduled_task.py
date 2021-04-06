from abc import abstractmethod


class ScheduledTask:
    @abstractmethod
    def start(self):
        pass
