import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/count_forward.csv'

rev_results = []
failed = []
curr_failed = False

curr_user_id = ''
curr_project_id = '0'
curr_task = '0'

recovery_count = 0


with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reversed(list(reader)):
        if(not (row['user_id'] == curr_user_id and row['project_id'] == curr_project_id and row['task'] == curr_task)):
            curr_user_id = row['user_id']
            curr_project_id = row['project_id']
            curr_task = row['task']

            recovery_count = 0

        curr_recovery_count = int(row['count_since_last_would_compile'])
        if curr_recovery_count > recovery_count:
            recovery_count = curr_recovery_count
        if row['would_compile'] == 'True':
            recovery_count = 0
        row['recovery_left'] = recovery_count - curr_recovery_count
        row['recovery_total'] = recovery_count
        rev_results.append(row)


results = list(reversed(rev_results))
keys = results[0].keys()
with open('transformed_data/count_backward.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
