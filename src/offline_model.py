import datetime as dt
import numpy as np

from data import get_hour_data, get_week_data


class OfflineModel:

    def __init__(self, country, hour_data=None, week_data=None):
        self.country = country
        self.hour_data = hour_data if hour_data is not None else get_hour_data()
        self.week_data = week_data if week_data is not None else get_week_data()

    def best_24h_start_point(self, task):
        """
        Find best start point in the coming 24 hours.
        :return: Best start hour in the coming 24 hours.
        """
        costs = []
        day_cost = sum(self.hour_data)
        for i in range(24):
            # Add hour costs for whole days, only for tasks longer than 24h.
            cost = day_cost * task.duration.days
            # Add hour costs for shorter periods
            hrs = task.duration.seconds // 3600
            if i + hrs <= 24:
                cost += sum(self.hour_data[i:i + hrs])
            else:
                hrs_left = (i + hrs) % 24
                cost += sum(self.hour_data[i:i + (hrs - hrs_left)])
                cost += sum(self.hour_data[:hrs_left])
            costs.append(cost)
        min_cost = np.amin(costs)
        min_start_point = np.argmin(costs)
        print("Lowest carbon cost:", min_cost, " When started at hour:", min_start_point)
        return min_start_point

    def best_week_start_point(self, task):
        """
        Find best start point in the coming 7 days.
        :return: Best start hour in the 7 days, .
        """

        # Structure data array to start from start hour index
        start_index = task.start.hour + task.start.weekday() * 24
        data = self.week_data.flatten()
        data = np.concatenate([data[start_index:], data[:start_index]])

        # Calculate size of search space
        time_left = task.deadline - task.start
        hours_left = time_left.total_seconds() // 3600
        # If we have more than a week left to schedule the task,
        # we find the best place in the coming week, since all weeks are the same.
        search_space = int(min(hours_left, len(data)))

        costs = []
        duration_in_hours = task.duration.seconds // 3600
        duration_in_weeks = task.duration.days // 7
        week_cost = sum(data)

        for i in range(search_space):
            # Sum the carbon from start point i until completion of the task
            data_from_i = np.concatenate([data[i:], data[:i]])
            cost = sum(data_from_i[:duration_in_hours])
            # If duration is longer than a whole week
            cost += week_cost * duration_in_weeks
            costs.append(cost)

        # Extract optimal start time
        min_cost = np.amin(costs)
        min_cost_hour = int(np.argmin(costs))
        # Add the number of hours for the best start time to the start date.
        best_start = task.start + dt.timedelta(hours=min_cost_hour)
        print("Lowest carbon cost:", min_cost, " When started at:", best_start)

        return best_start

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
            starting_points.append(self.best_week_start_point(task))
        return starting_points


if __name__ == '__main__':
    offline_model = OfflineModel("NL")
