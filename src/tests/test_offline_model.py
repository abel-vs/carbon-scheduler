import unittest
import datetime as dt
import numpy as np

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

increase_week_data = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47],
    [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71],
    [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],
    [96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
    [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143],
    [144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167]
]


class TestOfflineModel(unittest.TestCase):

    def test_best_24h_start_point_increasing_hours(self):
        model = OfflineModel(data=np.array(increase_hour_data))
        for task in tasks:
            self.assertEqual(model.best_24h_start_point(task.duration), 0, "Should be 0")

    def test_best_week_start_point_increasing_hours(self):
        model = OfflineModel(data=np.array(increase_week_data))
        for task in tasks:
            self.assertEqual(model.best_week_start_point(task.duration), 0, "Should be 0")


if __name__ == '__main__':
    unittest.main()
