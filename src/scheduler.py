import argparse
import datetime
import os
from src.offline_model import OfflineModel
import pickle
import subprocess
import time
import croniter
from crontab import CronTab, CronItem
from src.task import Task

program_name = 'Carbon Scheduler'
pickle_file = 'carbonstats.pickle'
user = 'arsen'


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
                        action='store_true',  # so default = False
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
                        action='store_true',  # so default = False
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


def list_jobs(cron, args):
    print("All scheduled jobs:")
    print()
    print("Repeating jobs:")
    for (idx, job) in enumerate(cron):
        now = datetime.datetime.now()
        cron = croniter.croniter(str(job.slices.render()), now)
        next_run = cron.get_next(datetime.datetime)
        print(f' Id: {idx:2}| Next run: {next_run} | Job: {str(job):10}')
    print()
    cmd = 'atq'
    result = subprocess.check_output(cmd, universal_newlines=True)
    print("One-off jobs:")
    print(result)


def cancel_repeating(cron, args):
    print("Repeating jobs:")
    for (idx, job) in enumerate(cron):
        print(idx, job)
    job_removed = None
    idx = 0
    for job in cron:
        # print(f"Comparing idx {idx} with our target {args.cancel_repeating}")
        if idx == int(args.cancel_repeating):
            if isinstance(job, CronItem):
                job_removed = job
                break
        idx = idx + 1

    if job_removed is not None:
        # this doesn't actually remove the job
        cron.remove(job_removed)
        print(f'Cancelled repeating job with id: {args.cancel_repeating:2} and command: {str(job_removed):10}')

    print("Repeating jobs:")
    idx = 0
    for job in cron:
        print(f' Id: {idx:2}| Job: {str(job):10}')
        idx = idx + 1


def cancel_one(args):
    subprocess.call(["at", "-r", str(args.cancel_one)], shell=False)
    print(f'Cancelled one-off job with id: {args.cancel_one:2}')


def schedule_repeating(cron, args):
    output_file = '/tmp/cron.lst'
    if args.output is not None:
        output_file = args.output
    output_file = output_file + ' 2>&1'  # send both stdout and stderr to our output file

    duration = datetime.timedelta(seconds=3600)  # in seconds
    if args.span is not None:
        duration = datetime.timedelta(seconds=int(args.span))

    deadline = datetime.datetime.now() + datetime.timedelta(days=7)
    if args.deadline is not None:
        deadline = datetime.datetime.now() + datetime.timedelta(seconds=int(args.deadline))

    model = OfflineModel('NL')
    task = Task(duration, deadline, datetime.datetime.now())
    new_start, stats = model.process_concurrently([task])[0]

    # we have a repeating job, schedule using `cron`

    # extra parentheses around the strings to get a multiline string without whitespace
    # see: https://stackoverflow.com/a/10660443
    item = CronItem.from_line((f'{args.repeat} python {os.path.abspath(args.job)} >> '
                               f'{output_file}'), cron=cron)
    cron.append(item)
    cron.write()
    next_run = croniter.croniter(args.repeat, datetime.datetime.now()).get_next(datetime.datetime)
    print(f'scheduled repeating job with schedule {args.repeat} - next run at {next_run}')


def schedule_one(args):
    output_file = '/tmp/cron.lst'
    if args.output is not None:
        output_file = args.output
    output_file = output_file + ' 2>&1'  # send both stdout and stderr to our output file

    duration = datetime.timedelta(seconds=3600)  # in seconds
    if args.span is not None:
        duration = datetime.timedelta(seconds=int(args.span))

    deadline = datetime.datetime.now() + datetime.timedelta(days=7)
    if args.deadline is not None:
        deadline = datetime.datetime.now() + datetime.timedelta(seconds=int(args.deadline))

    model = OfflineModel('NL')
    task = Task(duration, deadline, datetime.datetime.now())
    new_start, stats = model.process_concurrently([task])[0]

    # we have a one-off job, schedule using `at`
    format = '%Y%m%d%H%M'  # at's format:[[CC]YY]MMDDhhmm
    if args.green is False:
        time_str = new_start.strftime(format)
    else:
        time_str = datetime.datetime.now.strftime(format)
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
    print(f'🌱 Optimizing schedule to lower carbon emissions... 🌱')
    time.sleep(3)
    print(f'Scheduled one-off job for {time_string}')

    original_start = stats['original_start']
    new_start = stats['optimized_start']
    reduction = stats['reduction']
    original_cost = stats['original_cost']
    optimized_cost = stats['optimized_cost']

    totals = None
    try:
        with open(pickle_file, 'rb') as handle:
            totals = pickle.load(handle)
    except:
        data = {'original_cost': original_cost, 'optimized_cost': optimized_cost}
        try:
            with open(pickle_file, 'wb') as handle:
                pickle.dump(data, handle)
        except:
            print("Couldn't read statistics file")

        totals = data

    original_cost_total = totals['original_cost']
    optimized_cost_total = totals['optimized_cost']
    original_cost_total = original_cost_total + original_cost
    optimized_cost_total = optimized_cost_total + optimized_cost
    with open(pickle_file, 'wb') as handle:
        pickle.dump({'original_cost': original_cost_total,
                     'optimized_cost': optimized_cost_total},
                    handle)

    dateformat = "%Y-%m-%d %H:%M:%S"
    print((f'🌱 Rescheduling from {original_start.strftime(dateformat)} to {new_start.strftime(dateformat)} '
           f'will reduce CO2 intensity by {reduction:.2f}% 🌱'))
    print((f'🌱 Rescheduling has reduced your total carbon intensity from {original_cost_total}'
           f' gCO2/kWh to {optimized_cost_total} gCO2/kWh'
           f' (-{(1.0 - (float(optimized_cost_total) / float(original_cost_total))) * 100 :.2f}%) 🌱'))


def main():
    args = parse_args()

    cron = CronTab(user=user)

    if args.list:
        list_jobs(cron, args)
    elif args.cancel_repeating is not None:
        cancel_repeating(cron, args)
    elif args.cancel_one is not None:
        cancel_one(args)
    else:
        if args.repeat is not None:
            schedule_repeating(cron, args)
        elif args.at is not None:
            schedule_one(args)
        else:
            print('error: one of the following arguments is required: repeat, at')


if __name__ == '__main__':
    main()
