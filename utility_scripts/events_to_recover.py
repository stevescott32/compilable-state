import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/orig_error_line.csv'

results = []
data = []

curr_user_id = ''
curr_project_id = '0'
curr_task = '0'


count_since_last_success = 0
count_since_last_run = 0
count_since_last_would_compile = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

for index, row in enumerate(data):
    if row['would_compile'] == 'False':
        working_index = index
        curr_error_id = row['curr_error_id']
        working_row = row
        events_to_recover = 0
        while curr_error_id in working_row['curr_errors']:
            events_to_recover = events_to_recover + 1
            working_index = working_index + 1
            if working_index >= len(data):
                break
            working_row = data[working_index]
        row['events_to_recover'] = events_to_recover
    else:
        row['events_to_recover'] = 0


keys = data[0].keys()
with open('transformed_data/events_to_recover.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
