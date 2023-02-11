'''
'''

import ast
import csv
import os
import sys
import subprocess
import astboom

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

print('Running script ast viz')

class RemoveMismatchException(Exception):
    pass

def get_file_identifier(edit_event):
    return edit_event['SubjectID'] + edit_event['AssignmentID'] + edit_event['CodeStateSection']

def apply_event(file, edit_event):
    code_added = edit_event['InsertText']
    code_removed = edit_event['DeleteText']

    if code_added == '' and code_removed == '':
        return file

    if edit_event['SourceLocation'] == '':
        return file

    edit_position = int(float(edit_event['SourceLocation']))
    planned_remove = file[edit_position: edit_position + len(code_removed)]
    if not planned_remove == code_removed:
        raise RemoveMismatchException("Code removed doesn't match event")
    result = file[:edit_position] + code_added + file[edit_position + len(code_removed):]
    return result

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

# adapted from https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 2)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 


cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/filter_sort.csv'

files = {}
file_is_broken = {}
final_event_compiles = {}
results = []
current_subject = ''
status_message = ''
file_id = None
last_ast = None

i = 0

def filter_results(row):
    file_id = get_file_identifier(row)
    return final_event_compiles[file_id] and (not file_is_broken[file_id])

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        # if we have a new user, clear out the files that we don't need anymore
        if not row['SubjectID'] == current_subject:
            files = {}
            current_subject = row['SubjectID']


        file_id = get_file_identifier(row)
        # if the file already broke, skip it. It's ability to compile can't really be trusted
        if file_id in file_is_broken and file_is_broken[file_id]:
            continue
        # initialize the file if it hasn't been initialized yet
        if not file_id in files:
            files[file_id] = ''
        # track whether the file is broken
        if not file_id in file_is_broken:
            file_is_broken[file_id] = False
        if not file_id in final_event_compiles:
            final_event_compiles[file_id] = False
        try:
            # apply the next event and see if the file compiles
            files[file_id] = apply_event(files[file_id], row)
            compile_result = compile_program(files[file_id])
            row['would_compile'] = compile_result['compile_successful']
            row['error_message'] = compile_result['error_message']

            final_event_compiles[file_id] = compile_result['compile_successful']

            if compile_result['compile_successful']:
                one_ast = ast.parse(files[file_id])
                if not one_ast == last_ast and len(one_ast.body) > 0:
                    result = subprocess.run(['astboom', 'ast', files[file_id]], stdout=subprocess.PIPE)
                    print(result.stdout.decode('utf-8'))
                    last_ast = one_ast


        except RemoveMismatchException:
            file_is_broken[file_id] = True
            pass

        i += 1
        if i % 1000 == 0:
            progress(i, 14497464, status_message)
