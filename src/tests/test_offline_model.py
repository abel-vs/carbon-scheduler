import unittest
import datetime as dt

from offline_model import OfflineModel
from task import Task


# Test day = 19:00, 14 March 2022
today = dt.datetime(year=2022, month=3, day=14, hour=19)
# List of tasks
tasks = [
    Task(deadline=dt.datetime(2022, 3, 14, hour=23), duration=dt.timedelta(hours=1)),
    Task(deadline=dt.datetime(2022, 3, 18, hour=8), duration=dt.timedelta(hours=2)),
    Task(deadline=dt.datetime(2022, 3, 16, hour=8), duration=dt.timedelta(hours=5)),
    Task(deadline=dt.datetime(2022, 3, 16, hour=8), duration=dt.timedelta(hours=13)),
    Task(deadline=dt.datetime(2022, 3, 16, hour=8), duration=dt.timedelta(hours=24)),
    Task(deadline=dt.datetime(2022, 3, 16, hour=8), duration=dt.timedelta(hours=100)),
]

# Dummy data
increase_hour_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]


class TestOfflineModel(unittest.TestCase):

    def test_best_start_point_increasing_hours(self):
        model = OfflineModel(data=increase_hour_data)
        for task in tasks:
            self.assertEqual(model.best_start_point(task.duration), 0, "Should be 0")


if __name__ == '__main__':
    unittest.main()
