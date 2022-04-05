from datetime import datetime, timedelta

from PyInquirer import prompt, print_json
from prompt_toolkit.validation import Validator, ValidationError
from os.path import exists

import scheduler
from task import Task


class NumberValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))


class FileValidator(Validator):
    def validate(self, document):
        try:
            if not exists(document.text):
                raise ValidationError(message="File not found: " + document.text,
                                      cursor_position=len(document.text))
        except ValueError:
            raise ValidationError(message="Please enter path to file",
                                  cursor_position=len(document.text))


class DateValidator(Validator):
    def validate(self, document):
        try:
            date = datetime.strptime(document.text, '%d/%m/%y %H:%M')
            now = datetime.now()
            if date < now:
                raise ValidationError(message="Date has already passed: " + document.text,
                                      cursor_position=len(document.text))
        except ValueError:
            raise ValidationError(message="Please enter correct date and time (e.g. 28/7/23 8:00)",
                                  cursor_position=len(document.text))


welcome_question = {
    'type': 'list',
    'name': 'choice',
    'message': 'What would you like to do?',
    'choices': ["Schedule task", "View currently scheduled tasks", "View all tasks", "Help", "Close"]
}
task_question = {
    'type': "input",
    "name": "task",
    "message": "Task file (path from current location)",
    "validate": FileValidator,
}
duration_question = {
    'type': "input",
    "name": "duration",
    "message": "Duration of task (in hours)",
    "validate": NumberValidator,
    "filter": lambda val: timedelta(hours=float(val))
}
deadline_question = {
    'type': "input",
    "name": "deadline",
    "message": "Deadline for task (DD/MM/YY HH:mm)",
    "validate": DateValidator,
    "filter": lambda val: datetime.strptime(val, '%d/%m/%y %H:%M')
}
start_option_question = {
    'type': "list",
    "name": "choice",
    "message": "Earliest allowed execution time",
    'choices': ["Now", "Later"]
}
start_question = {
    'type': "input",
    "name": "start",
    "message": "Earliest start time (DD/MM/YY HH:mm)",
    "validate": DateValidator,
    "filter": lambda val: datetime.strptime(val, '%d/%m/%y %H:%M')
}

help_question = {'type': 'list',
                 'name': 'choice',
                 'message': 'What\'s your question?',
                 'choices': ["What is Carbon Scheduler?", "How to process multiple files?", "Back"],
                 }


def main_menu():
    option = prompt(welcome_question).get("choice")
    if option == "Schedule task":
        schedule_task_process()
    elif option == "View scheduled tasks":
        pass
    elif option == "View past tasks":
        pass
    elif option == "Help":
        help()
    else:
        print("Goodbye! 👋")


def schedule_task_process():
    file = prompt(task_question).get("task")
    duration = prompt(duration_question).get("duration")
    deadline = prompt(deadline_question).get("deadline")
    start = None
    if prompt(start_option_question).get("choice") == "Later":
        start = prompt(start_question).get("start")
    task = Task(duration, deadline, start)
    print("Scheduling task...")
    new_start, stats = scheduler.schedule_task(job=file, output_file="~/Desktop/output.txt", task=task)
    print("Task scheduled! 🥳\n"
          "Execution will start: ", new_start)


def help():
    option = prompt(help_question).get('choice')
    if option == "What is Carbon Scheduler?":
        print('Carbon Scheduler helps to schedule tasks in the most carbon-efficient way!')
        help()
    elif option == "How to process multiple files?":
        print("To Do")
        help()
    else:
        main_menu()
