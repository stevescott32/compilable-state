'''
'''

import csv
import os
import sys

# goal: read in deidentified grades

cwd = os.getcwd()
print(cwd)

csv.field_size_limit(sys.maxsize)

print('Loading data')
data_path = cwd + '/source_data' + '/grades-deidentified.csv'

results = []

projects = ['p4', 'p5', 'p6', 'p7', 'p8']

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for project in projects:
            split_result = {}
            split_result['user_id'] = row['user_id']
            split_result['project'] = project
            split_result['standardized_project'] = int(project[1:])
            split_result['grade'] = row[project]
            split_result['exam1'] = row['exam1']
            split_result['exam2'] = row['exam2']
            split_result['group'] = row['group']
            results.append(split_result)

keys = results[0].keys()
with open('transformed_data/grades/split_grades.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
