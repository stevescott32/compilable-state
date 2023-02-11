'''
The purpose of this script is to sort events so all events in a task
are grouped together
'''

import pandas as pd
import os

print('Running script sort_task')
cwd = os.getcwd()

events = pd.read_csv('./transformed_data/in_known_recovery.csv')
events = events.sort_values(by=['SubjectID', 'AssignmentID', 'X-Task', 'ClientTimestamp', 'unnamed_zero'], ignore_index=True)
events.to_csv(cwd + '/transformed_data' + '/sort_task.csv', index=False)
