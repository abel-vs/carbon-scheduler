import subprocess
import datetime
import argparse
import os
import sys
from crontab import CronTab, CronItem
import task

from apscheduler.schedulers.background import BackgroundScheduler

from offline_model import OfflineModel

def parse_args():
     # Create the parser

    parser = argparse.ArgumentParser(description='Carbon Scheduler v0.1')

    # Add the arguments
    parser.add_argument('job',
                       type=str,
                       help='the Python filename of the job to schedule')

    parser.add_argument('--repeat',
                       metavar='SCHEDULE',
                       type=str,
                       help='a cron expression or a natural language expression describing the \
                       repetition schedule of the job')

    parser.add_argument('--at',
                       metavar='DATE_SPECIFICATION',
                       type=str,
                       help='a string describing when to schedule the task')

    parser.add_argument('-t',
                        action='store_true', # so default = False
                        help='pass this flag if you set --at and you want to specify time \
                             absolutely instead of relatively') 

    parser.add_argument('--span', '--duration',
                       type=str,
                       help='the estimated span, or duration, of the job, in seconds',
                       required=False)

    parser.add_argument('--delay',
                       type=str,
                       help='minimum number of seconds that have to pass before starting task',
                       required=False)
    
    parser.add_argument('--deadline',
                       type=str,
                       help='the estimated deadline of the job, in seconds from now',
                       required=False)

    parser.add_argument('--output', '--o',
                       type=str,
                       help='the path to the output file',
                       required=False)

    parser.add_argument('-g', '-green', '-mybasementisfullofbatteries', '-mbifob', 
                        action='store_true', # so default = False
                        help='pass this flag if your computing infrastructure is fully \
                        carbon-neutral') 

    args = parser.parse_args()

    return args

if __name__ == '__main__':
        
    args = parse_args()

    cron = CronTab(user='wander')
    for job in cron:
        print(job)

    output_file = '~/Desktop/output.txt'
    if args.output is not None:
        output_file = args.output
    output_file = output_file + ' 2>&1'

    duration = datetime.timedelta(seconds=3600) # in seconds
    if args.span is not None:
        duration = datetime.timedelta(seconds=args.span)
    
    deadline = datetime.datetime.now() + datetime.timedelta(days=7)
    if args.deadline is not None:
        deadline = datetime.datetime.now() + datetime.timedelta(seconds=args.deadline)

    start = None
    if args.delay is not None:
        start = datetime.datetime.now() + datetime.timedelta(seconds=args.delay)

    model = OfflineModel('NL')
    task = task.Task(duration, deadline, start)
    new_start = model.process_concurrently([task])[0]

    print(new_start)

    if args.repeat is not None:
        # we have a repeating job, schedule using `cron`

        # extra parentheses around the strings to get a multiline string without whitespace
        # see: https://stackoverflow.com/a/10660443
        item = CronItem.from_line((f'{args.repeat} python {os.path.abspath(args.job)} >> '
                                    f'{output_file}'), cron=cron)
        cron.append(item)
        cron.write()
        print('scheduled repeating job')
    elif args.at is not None:
        # we have a one-off job, schedule using `at`
        time_str = new_start.strftime('%Y%m%d%H%M') # at's format:[[CC]YY]MMDDhhmm
        at_options = ""
        at_time = time_str
        if args.t is True:
            at_options = '-t'
            at_time = args.at
        cmd = (f'python {os.path.abspath(args.job)} >> {output_file} '
                f'| at {at_options} {at_time} >> /dev/null') #2>&1')
        subprocess.run(cmd, shell=True) # TODO: remove shell=True
        print('scheduled one-off job')
    else:
        print('error: one of the following arguments is required: repeat, at')
