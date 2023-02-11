import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/switches.csv'

results = []
failed = []
curr_failed = False

curr_user_id = ''
curr_project_id = '0'
curr_task = '0'


count_since_last_success = 0
count_since_last_run = 0
count_since_last_would_compile = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if(not (row['user_id'] == curr_user_id and row['project_id'] == curr_project_id and row['task'] == curr_task)):
            curr_user_id = row['user_id']
            curr_project_id = row['project_id']
            curr_task = row['task']

            count_since_last_run = 0
            count_since_last_success = 0
            count_since_last_would_compile = 0
        if row['change_type'] == 'TASK':
            pass
        elif row['change_type'] == 'setValue':
            pass
        elif row['change_type'] == 'RUN':
            count_since_last_run = 0
            if not row['has_error']:
                count_since_last_success = 0
                count_since_last_would_compile = 0
            pass
        elif row['change_type'] == 'SUBMIT':
            pass
        else:
            count_since_last_run += 1
            count_since_last_success += 1
            if row['would_compile'] == 'True':
                count_since_last_would_compile = 0
            else:
                count_since_last_would_compile += 1
        row['count_since_last_run'] = count_since_last_run
        row['count_since_last_success'] = count_since_last_success
        row['count_since_last_would_compile'] = count_since_last_would_compile
        results.append(row)


keys = results[0].keys()
with open('transformed_data/count_forward.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
