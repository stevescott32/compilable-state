# TODO:
# x decide sorting strategy
# x assume that empty file = known would compile
# - flag each time they run the program and it doesn't compile as known would not compile
#   - multiple files compiling/running together

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

print('Running last run would compile script')

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/sort_file.csv'

results = []
current_subject = ''
last_run_would_compile = True

i = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('transformed_data/last_run_would_compile.csv', 'w', newline='')  as output_file:
        dict_writer = None # csv.DictWriter(output_file, keys)

        for row in reader:
            row['last_run_would_compile'] = last_run_would_compile
            if row['EventType'] == 'Run.Program':
                last_run_would_compile = row['would_compile'] == 'True'

            if not row['SubjectID'] == current_subject:
                current_subject = row['SubjectID']
                # assumption: switching subjects indicates a clean start. Until they run the program the first time,
                # the last_run_would_compile column should be true
                last_run_would_compile = True 
                row['last_run_would_compile'] = last_run_would_compile
                if i == 0:
                    # set up the dictionary writer
                    keys = row.keys()
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                elif i > 0:
                    dict_writer.writerows(results)
                    results = []

            i += 1
            results.append(row)

        # write the final chunk of rows
        dict_writer.writerows(results)

