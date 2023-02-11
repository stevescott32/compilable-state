'''
'''

import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

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


cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/filter_sort.csv'

files = {}
file_is_broken = {}
final_event_compiles = {}
results = []

i = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # only consider rows that are edit events for files
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
            results.append(row)

        except RemoveMismatchException:
            file_is_broken[file_id] = True
            pass

        i += 1
        if i % 10000 == 0:
            fail_count = 0
            for key in file_is_broken:
                if file_is_broken[key] == True:
                    fail_count = fail_count + 1
            print(f'{fail_count} out of {len(file_is_broken)} files are broken: {100 * fail_count / len(file_is_broken)} %')
            print(i)


def filter_results(row):
    file_id = get_file_identifier(row)
    return final_event_compiles[file_id] and (not file_is_broken[file_id])

print(len(results))
results = list(filter(filter_results, results))
print(len(results))

keys = results[0].keys()
with open('transformed_data/compile_every_event.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)

# failed_keys = failed[0].keys()
# with open('results/failed_events.csv', 'w', newline='')  as output_file:
#     dict_writer = csv.DictWriter(output_file, failed_keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(failed)

