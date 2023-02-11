import csv
import os
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

cwd = os.getcwd()
print(cwd)

print('Loading data')
data_path = cwd + '/transformed_data' + '/count_backward.csv'

results = []
with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['error_line'] == '' or row['startLine'] == '':
            row['dist_edit_to_error'] = 0
        else:
            # error line is 1 based, start line is 0 based, so subtract one from error line
            error_line = int(row['error_line']) - 1
            start_line = int(float(row['startLine']))
            row['dist_edit_to_error'] = start_line - error_line
        results.append(row)


keys = results[0].keys()
with open('transformed_data/dist_edit_to_error.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
