import pickle
import subprocess
import datetime
import argparse
import os
from crontab import CronTab, CronItem
import task
import croniter
import time

from apscheduler.schedulers.background import BackgroundScheduler

from offline_model import OfflineModel

program_name = 'Carbon Scheduler'

def parse_args():
     # Create the parser

    parser = argparse.ArgumentParser(description=f'{program_name} v0.1')

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

    args = parser.parse_args()

    return args

if __name__ == '__main__':
        
    args = parse_args()

    cron = CronTab(user='wander')

    output_file = '~/Desktop/output.txt'
    if args.output is not None:
        output_file = args.output
    output_file = output_file + ' 2>&1' # send both stdout and stderr to our output file

    duration = datetime.timedelta(seconds=3600) # in seconds
    if args.span is not None:
        duration = datetime.timedelta(seconds=args.span)
    
    deadline = datetime.datetime.now() + datetime.timedelta(days=7)
    if args.deadline is not None:
        deadline = datetime.datetime.now() + datetime.timedelta(seconds=int(args.deadline))

    model = OfflineModel('NL')
    task = task.Task(duration, deadline, datetime.datetime.now())
    new_start, stats = model.process_concurrently([task])[0]

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
        format = '%Y%m%d%H%M' # at's format:[[CC]YY]MMDDhhmm
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
        subprocess.run(cmd, shell=True) # TODO: remove shell=True

        time_string = args.at
        if args.t is True:
            time_string = new_start.strftime("%Y-%m-%d %H:%M:%S")
        print(f'Optimizing schedule to lower carbon emissions...')
        time.sleep(3)
        print(f'Scheduled one-off job for {time_string}')

        original_start = stats['original_start']
        new_start = stats['optimized_start']
        reduction = stats['reduction']
        saved_carbon = stats['original_cost'] - stats['optimized_cost']

        with open('carbon_stats.pickle', 'rb') as handle:
            stats = pickle.load(handle)
            total_carbon = stats['total_carbon']
            with open('carbon_stats.pickle', 'wb') as handle:
                pickle.dump({'total_carbon': saved_carbon}, handle)

        print(f'Rescheduling from {original_start} to {new_start} will reduce CO2 intensity by {reduction:.2f}%')
    else:
        print('error: one of the following arguments is required: repeat, at')
