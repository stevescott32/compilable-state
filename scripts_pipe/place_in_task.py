import csv
import sys
from typing import Generator
import pandas as pd

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

print('Running place in task script')

def yield_tasks(event_file_path: str) -> Generator:
    """
    Create a generator that yields the events associated with each task
    """
    current_subject = ''
    current_assignment = ''
    current_file = ''
    current_task = ''

    events_in_task = []

    with open(event_file_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)

        current_event = next(reader)

        while(current_event):
            if (current_event['SubjectID'] == current_subject \
                and current_event['AssignmentID'] == current_assignment \
                and current_event['CodeStateSection'] == current_file \
                and current_event['X-Task'] == current_task) \
                :
                events_in_task.append(current_event)
                current_event = next(reader, None)
            else:
                if len(events_in_task) > 0:
                    yield events_in_task

                events_in_task = [current_event]
    
                # set up for the next iteration
                current_subject = current_event['SubjectID']
                current_assignment = current_event['AssignmentID']
                current_file = current_event['CodeStateSection']
                current_task = current_event['X-Task']

                current_event = next(reader, None)


task_generator = yield_tasks('transformed_data/next_event_type.csv')
task_events = next(task_generator)

with open('transformed_data/place_in_task.csv', 'w', newline='')  as output_file:

        task_events[0]['place_in_task'] = 1 / len(task_events)

        dict_writer = csv.DictWriter(output_file, task_events[0].keys())
        dict_writer.writeheader()

        while(task_events):
            for i, event in enumerate(task_events):
                event['place_in_task'] = (i + 1) / len(task_events)

            # write results for this user + assn + file to disk
            dict_writer.writerows(task_events)
            task_events = next(task_generator, None)
