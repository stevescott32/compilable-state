'''
'''

import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

print('Running script switches')

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/compile_every_event.csv'

results = []
current_subject = ''
status_message = ''
last_would_compile = True

i = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('transformed_data/switches.csv', 'w', newline='')  as output_file:
        dict_writer = None # csv.DictWriter(output_file, keys)

        for row in reader:
            # populate the switch columns
            current_would_compile = row['would_compile'] == 'True'
            row['switch_to_success'] = not last_would_compile and current_would_compile
            row['switch_to_fail'] = last_would_compile and not current_would_compile
            last_would_compile = current_would_compile

            if not row['SubjectID'] == current_subject:
                current_subject = row['SubjectID']
                if i == 0:
                    # set up the dictionary writer
                    keys = row.keys()
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                elif i > 0:
                    dict_writer.writerows(results)
                    results = []

            # only consider rows that are edit events for files
            i += 1
            results.append(row)

        # write the final chunk of rows
        dict_writer.writerows(results)

