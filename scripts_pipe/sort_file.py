'''
The purpose of this script is to sort events so all events in a file
are grouped together
'''

import pandas as pd
import os

print('Running script sort_file')
cwd = os.getcwd()

events = pd.read_csv('./transformed_data/switches.csv')
events = events.sort_values(by=['SubjectID', 'AssignmentID', 'CodeStateSection', 'X-Task', 'ClientTimestamp', 'unnamed_zero'], ignore_index=True)
events.to_csv(cwd + '/transformed_data' + '/sort_file.csv', index=False)
