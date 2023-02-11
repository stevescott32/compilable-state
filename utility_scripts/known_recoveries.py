import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/dist_edit_to_error.csv'

results = []
failed = []
curr_failed = False

curr_user_id = ''
curr_project_id = '0'
curr_task = '0'

in_recovery = False


with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if(not (row['user_id'] == curr_user_id and row['project_id'] == curr_project_id and row['task'] == curr_task)):
            curr_user_id = row['user_id']
            curr_project_id = row['project_id']
            curr_task = row['task']
            in_recovery = False
        if(row['switch_success_fail']):
            in_recovery = True
        if in_recovery:
            if row['would_compile'] == 'True':
                in_recovery = False
            else:
                results.append(row)


keys = results[0].keys()
with open('transformed_data/known_recoveries.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
