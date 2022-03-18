from datetime import datetime
import argparse
import time
import os
import sys
from crontab import CronTab

from apscheduler.schedulers.background import BackgroundScheduler


def train_model():
    print('dask train_model! The time is: %s' % datetime.now())


if __name__ == '__main__':
    
    argumentList = sys.argv[1:]
    
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Schedule Python tasks')

    # Add the arguments
    my_parser.add_argument('job',
                       metavar='job',
                       type=str,
                       help='the Python filename of the job to schedule')

    my_parser.add_argument('--span',
                       metavar='span',
                       type=str,
                       help='the estimated span, or duration, of the job, in seconds',
                       required=False)

    my_parser.add_argument('--deadline',
                       metavar='deadline',
                       type=str,
                       help='the estimated deadline of the job, in seconds from now',
                       required=False)

    # Execute the parse_args() method
    args = my_parser.parse_args()

    cron = CronTab(user='wander')
    job = cron.new(command=f'python {os.path.abspath(args.job)} >> ~/Desktop/output2.txt 2>&1')
    
    job.minute.every(1)
    cron.write()

