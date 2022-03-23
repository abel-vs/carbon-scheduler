import datetime as dt


class Task:
    def __init__(self, duration, deadline, start=None):
        self.duration = duration
        self.deadline = deadline
        self.start = start or dt.datetime.now()
        if self.deadline < self.start:
            raise Exception("Deadline has already passed." if start is None else "Deadline is before start.")
        if self.duration > (self.deadline - self.start):
            raise Exception("Not enough time to complete the task before the deadline.")
