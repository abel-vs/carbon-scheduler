import datetime

import numpy as np
import pandas as pd

from data import get_hour_data


class OfflineModel:

    def __init__(self):
        self.data = get_hour_data()

    def get_current_carbon(self):
        """
        Get the carbon intensity of the current hour.
        """
        now = datetime.datetime.now()
        return self.data[now.hour]

    def get_lowest_carbon(self):
        """
        For tasks taking less than an hour.
        :return: Hour with lowest carbon intensity.
        """
        return np.argmin(self.data)

    def process_all_consecutive(self, tasks):
        """
        Processes all tasks consecutively in the most carbon efficient way.
        The task schedules may not overlap.
        All tasks should be handled before their deadlines.
        :param tasks: List of tasks, being tuples of a duration and a deadline.
        :return: One starting point for processing the whole batch of tasks.
        """
        pass

    def process_distributed(self, tasks):
        """
        Processes all tasks in the most carbon efficient way, without overlapping
        The task schedules don't have to be executed consecutively, meaning the program may be idle during the worst hours.
        The task schedules may not overlap.
        All tasks should be handled before their deadlines.
        :param tasks: List of tasks, being tuples of a duration and a deadline.
        :return: List of starting points for each task
        """
        pass

    def process_concurrently(self, tasks):
        """
        Processes all tasks on their optimal time, possibly concurrently.
        This means for each task it searches the best possible time to execute before the deadline.
        The task schedules may overlap.
        :param tasks: List of tasks, being tuples of a duration and a deadline.
        :return: List of starting points for each task
        """
        starting_points = []
        for task in tasks:
            starting_points.append(self.get_lowest_carbon(task))
        return starting_points


if __name__ == '__main__':
    offline_model = OfflineModel()
