'''
The purpose of this script is to add the `standardized_project` column,
which standardizes project ids to allow direct comparisons between projects
from the test and control semesters
'''

import pandas as pd
import os

cwd = os.getcwd()
print(cwd)

def get_standardized_project(row):
    lookup = {
        128: 4,
        129: 4, 
        195: 4, 
        130: 5,
        131: 5,
        200: 5,
        132: 6,
        133: 6,
        204: 6,
        134: 7,
        135: 7,
        205: 7,
        136: 8,
        138: 8,
        207: 8,
    }

    project_id = row['project_id']
    if project_id in lookup:
        return lookup[row['project_id']]
    else:
        return -1

df = pd.read_csv('./source_data/project-events.csv')

df['standardized_project'] = df.apply(get_standardized_project, axis=1)

df.to_csv(cwd + '/transformed_data' + '/standardized_project.csv', index=False)
