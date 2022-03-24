import subprocess
import datetime
import argparse
import os
import sys
from crontab import CronTab, CronItem
import task

from apscheduler.schedulers.background import BackgroundScheduler

from offline_model import OfflineModel

if __name__ == '__main__':
    
    argumentList = sys.argv[1:]
    
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Schedule Python tasks')

    # Add the arguments
    my_parser.add_argument('job',
                       metavar='job',
                       type=str,
                       help='the Python filename of the job to schedule')

    my_parser.add_argument('--repeat',
                       metavar='repeat',
                       type=str,
                       help='a cron expression or a natural language expression describing the \
                       repetition schedule of the job')

    my_parser.add_argument('--at',
                       metavar='at',
                       type=str,
                       help='a natural language string describing when to schedule the task')

    my_parser.add_argument('--span', '--duration',
                       metavar='span',
                       type=str,
                       help='the estimated span, or duration, of the job, in seconds',
                       required=False)

    my_parser.add_argument('--not-before',
                       metavar='not_before',
                       type=str,
                       help='minimum number of seconds that have to pass before starting task',
                       required=False)
    
    my_parser.add_argument('--deadline',
                       metavar='deadline',
                       type=str,
                       help='the estimated deadline of the job, in seconds from now',
                       required=False)

    my_parser.add_argument('--output', 'o',
                       metavar='output',
                       type=str,
                       help='the path to the output file',
                       required=False)

    args = my_parser.parse_args()

    cron = CronTab(user='wander')
    for job in cron:
        print(job)

    output_file = '~/Desktop/output.txt'
    if args.output is not None:
        output_file = args.output
    output_file.append(' 2>&1')

    duration = datetime.timedelta(seconds=10) # in seconds
    if args.span is not None:
        duration = datetime.timedelta(seconds=args.span)
    
    deadline = datetime.datetime.now() + datetime.timedelta(days=7)
    if args.deadline is not None:
        deadline = datetime.datetime.now() + datetime.timedelta(seconds=args.deadline)

    start = None
    if args.not_before is not None:
        start = datetime.datetime.now() + datetime.timedelta(seconds=args.not_before)

    model = OfflineModel('NL')
    task = task.Task(duration, deadline, start)
    new_start = model.process_concurrently([task])[0]

    print(new_start)

    if args.repeat is not None:
        # we have a repeating job, schedule using `cron`
        #job = cron.new(command=f'python {os.path.abspath(args.job)} >> {output_file}')
        #job.minute.every(1)

        item = CronItem.from_line(f'{args.repeat} python {os.path.abspath(args.job)} >> \
            {output_file}', cron=cron)
        cron.append(item)
        cron.write()
        print('scheduled repeating job')
    elif args.at is not None:
        # we have a one-off job, schedule using `at`
        time_str = new_start.strftime('%Y%m%d%H%M') # [[CC]YY]MMDDhhmm

        print('new start: ' + str(new_start))
        cmd = f'python {os.path.abspath(args.job)} >> {output_file}\
             | at {args.at} >> /dev/null 2>&1'
        subprocess.run(cmd, shell=True) # TODO: remove shell=True
        print('scheduled one-off job')
    else:
        print('error: one of the following arguments is required: repeat, at')
