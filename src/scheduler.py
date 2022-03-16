from datetime import datetime
import argparse
import time
import os
import sys
from subprocess import Popen

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

    input_path = args.job
    print(input_path)

    scheduler = BackgroundScheduler()
    scheduler.add_job(train_model, 'date')
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
            # print("you entered " + input("input smth"))
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

