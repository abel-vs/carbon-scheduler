from subprocess import check_output
import argparse
import os
import sys
from crontab import CronTab, CronItem
from croniter import croniter
from datetime import datetime
import task
import croniter

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

    parser.add_argument('-green', '-g', '-mybasementisfullofbatteries', '-mbifob', 
                        action='store_true', # so default = False
                        help='pass this flag if your computing infrastructure is fully \
                        carbon-neutral')

    parser.add_argument('--list', '-l',
                         action='store_true',
                         help="list all scheduled jobs")

    parser.add_argument('--cancel_repeating', '-cr',
                        type=int,
                        help="Cancel repeating job given the id")

    parser.add_argument('--cancel_one', '-co',
                        type=int,
                        help="Cancel one-off job given the id")

    args = parser.parse_args()

    return args

if __name__ == '__main__':
        
    args = parse_args()

    cron = CronTab(user='arsen')

    output_file = '/tmp/cron.lst'
    if args.output is not None:
        output_file = args.output

    output_file = output_file + ' 2>&1' # send both stdout and stderr to our output file

    if args.list:
        print("All scheduled jobs:")
        print()
        print("Repeating jobs:")
        for (idx, job) in enumerate(cron):
            now = datetime.now()
            next_run = croniter(str(job.slices.render()), now).get_next(datetime)
            print(f' Id: {idx:2}| Next run: {next_run} | Job: {str(job):10}')
        print()
        cmd = 'atq'
        result = check_output(cmd, universal_newlines=True)
        print("One-off jobs:")
        print(result)
    elif args.cancel_repeating is not None:
        job_removed = None
        for (idx, job) in enumerate(cron):
            if idx == args.cancel_repeating:
                job_removed = job

        if job_removed is not None:
            cron.remove(job_removed)
            cron.write()
            print(f'Cancelled repeating job with id: {args.cancel_repeating:2} and command: {str(job_removed):10}')
    elif args.cancel_one is not None:
        cmd = f'atq -r {args.cancel_one}'
        result = check_output(cmd, universal_newlines=True)
        print(f'Cancelled one-off job with id: {args.cancel_one:2}')
    else:
        duration = datetime.timedelta(seconds=3600) # in seconds
        if args.span is not None:
            duration = datetime.timedelta(seconds=args.span)

        deadline = datetime.datetime.now() + datetime.timedelta(days=7)
        if args.deadline is not None:
            deadline = datetime.datetime.now() + datetime.timedelta(seconds=args.deadline)

        delay = datetime.datetime.now()
        if args.delay is not None:
            delay = datetime.datetime.now() + datetime.timedelta(seconds=args.delay)

        model = OfflineModel('NL')
        task = task.Task(duration, deadline, delay)
        new_start = model.process_concurrently([task])[0]

        print("Task scheduled at", new_start)

        if args.repeat is not None:
            # we have a repeating job, schedule using `cron`

            # extra parentheses around the strings to get a multiline string without whitespace
            # see: https://stackoverflow.com/a/10660443
            item = CronItem.from_line((f'{args.repeat} python {os.path.abspath(args.job)} >> '
                                       f'{output_file}'), cron=cron)
            cron.append(item)
            cron.write()
            next_run = croniter.croniter(args.repeat, datetime.datetime.now()).get_next(datetime.datetime)
            print(f'scheduled repeating job with schedule {args.repeat} - next run at {next_run}')
        elif args.at is not None:
            # we have a one-off job, schedule using `at`
            format = '%Y%m%d%H%M'  # at's format:[[CC]YY]MMDDhhmm
            if args.green is False:
                time_str = new_start.strftime(format)
            else:
                time_str = delay.strftime(format)
            at_options = ""
            at_time = args.at
            if args.t is True:
                at_time = time_str
                at_options = '-t'
            cmd = (f'python {os.path.abspath(args.job)} >> {output_file} '
                   f'| at {at_options} {at_time} >> /dev/null 2>&1')
            subprocess.run(cmd, shell=True)  # TODO: remove shell=True

            time_string = args.at
            if args.t is True:
                time_string = new_start.strftime("%Y-%m-%d %H:%M:%S")
            print(f'Scheduled one-off job for {time_string}')
        else:
            print('error: one of the following arguments is required: repeat, at')
