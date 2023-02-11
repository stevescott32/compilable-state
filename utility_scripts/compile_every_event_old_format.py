'''
This script takes the sorted + filtered keystroke data and both attempts to 
recreate the file after every event AND attempts to compile that recreated
file after every event. It adds the `would_compile` and `error_message` columns
to the data.
'''

import csv
import os
import sys

class EventException(Exception):
    pass

class EventIndexException(EventException):
    pass

class RemoveMismatchException(EventException):
    pass

class AddMismatchException(EventException):
    pass

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

def file_to_string(file) :
    s = '\n'
    return s.join(file)

def string_to_file(s):
    return s.split('\n')

def convert_index(row, col, fauxFile):
    result = 0
    i = 0
    while i < row: 
        if i < len(fauxFile):
            result += len(fauxFile[i]) + 1
        else:
            raise EventIndexException(f'Warning in convert_index - i {i} is outside the range of file of length {str(len(fauxFile))}')
        i += 1
    result += col
    return result

def apply_event(e, fauxFile) :
    if e['change_type'] == 'setValue':
        return string_to_file(e['code_added'])

    startLine = int(float(e['startLine']))
    endLine = int(float(e['endLine']))
    startCol = int(float(e['startCol']))
    endCol = int(float(e['endCol']))

    serialized = file_to_string(fauxFile)
    startIndex = convert_index(startLine, startCol, fauxFile)
    endIndex = convert_index(endLine, endCol, fauxFile)

    begin = serialized[0:startIndex]
    removed = serialized[startIndex:endIndex]
    middle = e['code_added']
    end = serialized[endIndex:]
    if removed != e['code_removed']:
        raise RemoveMismatchException(
            f'Removed mismatch - event: {format_visible_whitespace(e["code_removed"])}, faux file: {format_visible_whitespace(removed)}')

    combined = begin + middle + end
    addedSubstring = combined[len(begin):len(begin) + len(e['code_added'])]
    if addedSubstring != e['code_added']:
        raise AddMismatchException(f'Code added mismatch - event: {format_visible_whitespace(e["code_added"])}, faux file: {format_visible_whitespace(addedSubstring)}')
    recreatedFile = string_to_file(combined)

    return recreatedFile

def format_visible_whitespace(s):
    return s.replace(' ', '•').replace('\t', '→')


def compile_program(program):
    result = {}
    try:
        compile(program, '', 'exec')
        result['compile_successful'] = True
        result['error_message'] = ''
    except Exception as e:
        result['compile_successful'] = False
        result['error_message'] = str(e)
    return result


def initialize_faux_file(row):
    if row['standardized_project'] == '4':
        return string_to_file("# Don't forget comments that go here\n")
    if row['standardized_project'] == '5':
        return string_to_file("# Task 1")
    elif row['standardized_project'] == '6':
        return string_to_file("""# Name
# Course
# Assn

'''
Software Development Process
'''
""")
    elif row['standardized_project'] == '7':
        return string_to_file("""
What are your thoughts on Phanon? 

Ideas to discuss:
    Did it help you learn? Did it not make a difference?
    We used it for approximately 1/2 of the semester. Would more or less be better?
    What could make it better?
    What were things you would change about it?

Answer Below
************\n\n\n
""")
    else:
        return []

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/filter_sort.csv'

faux_file = []
results = []
failed = []
curr_failed = False

curr_user_id = ''
curr_project_id = '0'
curr_task = '0'


i = 0
i_of_hw_start = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if(not (row['user_id'] == curr_user_id and row['project_id'] == curr_project_id and row['task'] == curr_task)):
            curr_user_id = row['user_id']
            curr_project_id = row['project_id']
            curr_task = row['task']
            faux_file = initialize_faux_file(row)
            curr_failed = False
            i_of_hw_start = i
        elif curr_failed:
            continue
        try:
            # apply the event, if necessary
            if (not row['change_type'] == 'TASK' 
                and not row['change_type'] == 'RUN'
                and not row['change_type'] == 'SUBMIT'
                and not row['change_type'] == 'setValue'
                ):
                faux_file = apply_event(row, faux_file)
            elif row['change_type'] == 'setValue':
                faux_file = string_to_file(row['code_added'])

            # check if the re-created file would compile after each event
            compile_result = compile_program(file_to_string(faux_file).encode())
            row['would_compile'] = compile_result['compile_successful']
            row['error_message'] = compile_result['error_message']
            results.append(row)

            # progress tracking
            i += 1
            if i % 10000 == 0:
                print(i)
        except EventException as e:
            row['num_successful'] = i - i_of_hw_start
            failed.append(row)
            curr_failed = True


keys = results[0].keys()
with open('transformed_data/compile_every_event.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)

failed_keys = failed[0].keys()
with open('results/failed_events.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, failed_keys)
    dict_writer.writeheader()
    dict_writer.writerows(failed)

