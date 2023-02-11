'''
Assumptions:
- Events are sorted so that all edits to a file are together
- The CodeStateSection column is accurate for Run.Program events
- Each Run.Program event was only running a single file
'''

import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

print('Running in known recovery script')

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/last_run_would_compile.csv'

results = []
current_subject = ''
last_event_in_recovery = False

i = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('transformed_data/in_known_recovery.csv', 'w', newline='')  as output_file:
        dict_writer = None # csv.DictWriter(output_file, keys)

        for row in reader:
            if not row['SubjectID'] == current_subject:
                current_subject = row['SubjectID']
                row['in_known_recovery'] = False
                last_event_in_recovery = False
                if i == 0:
                    # set up the dictionary writer
                    keys = row.keys()
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                elif i > 0:
                    dict_writer.writerows(results)
                    results = []


            last_run_would_compile = row['last_run_would_compile'] == 'True'
            current_would_compile = row['would_compile'] == 'True'

            start_recovery = row['EventType'] == 'Run.Program' and row['would_compile'] == 'False'
            continue_recovery = last_event_in_recovery and (not current_would_compile) and (not last_run_would_compile)
            in_known_recovery = start_recovery or continue_recovery
            row['in_known_recovery'] = in_known_recovery
            i += 1
            results.append(row)
            last_event_in_recovery = in_known_recovery

        # write the final chunk of rows
        dict_writer.writerows(results)

