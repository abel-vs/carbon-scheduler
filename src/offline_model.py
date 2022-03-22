import datetime as dt
import numpy as np
import pandas as pd

from data import get_hour_data

class OfflineModel:

    def __init__(self, data=None):
        if data is None:
            self.data = get_hour_data()
        else:
            self.data = data

    def get_current_carbon(self):
        """
        Get the carbon intensity of the current hour.
        """
        now = dt.datetime.now()
        return self.data[now.hour]

    def get_lowest_carbon(self):
        """
        For tasks taking less than an hour.
        :return: Hour with lowest carbon intensity.
        """
        return np.argmin(self.data)

    def best_start_point(self, duration: dt.timedelta):
        """
        Find best start point in the coming 24 hours.
        :return: Best start hour in the coming 24 hours.
        """
        costs = []
        day_cost = sum(self.data)
        # current_hour = dt.datetime.now().hour
        for i in range(24):
            # Add hour costs for whole days, only for tasks longer than 24h.
            cost = day_cost * duration.days
            # Add hour costs for shorter periods
            hrs = duration.seconds//3600
            if i + hrs <= 24:
                cost += sum(self.data[i:i + hrs])
            else:
                hrs_left = (i + hrs) % 24
                cost += sum(self.data[i:i+(hrs-hrs_left)])
                cost += sum(self.data[:hrs_left])
            costs.append(cost)
        min_cost = np.amin(costs)
        min_start_point = np.argmin(costs)
        print("Lowest carbon cost:", min_cost, " When started at hour:", min_start_point)
        return min_start_point

    @staticmethod
    def hours_until_deadline(deadline):
        """
        Get the number of hours until the deadline.
        :param deadline: in datetime format
        :return: Number of hours until the deadline.
        """
        now = dt.datetime.now()
        time = deadline - now
        time_in_s = time.total_seconds()
        hours = divmod(time_in_s, 3600)[0]
        return int(hours)

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
