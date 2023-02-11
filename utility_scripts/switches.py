import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/events_to_recover.csv'

curr_user_id = ''
curr_project_id = '0'
curr_task = '0'

results = []

last_run = {}
last_run['has_error'] = 'na'

# filter down to just run events
with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # if the user, task, or project has changed, reset so first run cannot be a switch
        if(not (row['user_id'] == curr_user_id and row['project_id'] == curr_project_id and row['task'] == curr_task)):
            curr_user_id = row['user_id']
            curr_project_id = row['project_id']
            curr_task = row['task']
            last_run = {}
            last_run['has_error'] = 'na'

        if row['change_type'] == 'RUN':
            row['switch_success_fail'] = (not row['has_error'] == 'na') and (row['has_error'] == 'True' and last_run['has_error'] == 'False')
            row['switch_fail_success'] = (not row['has_error'] == 'na') and (row['has_error'] == 'False' and last_run['has_error'] == 'True')
            last_run = row
        else:
            # non-run events shouldn't have a value
            row['switch_success_fail'] = ''
            row['switch_fail_success'] = ''
        results.append(row)


keys = results[0].keys()
with open('transformed_data/switches.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
