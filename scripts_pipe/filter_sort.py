'''
The purpose of this script is the filter and sort the initial project-events csv so
the events are sorted on timestamp
'''

import pandas as pd
import os

print('Running script filter_sort')
cwd = os.getcwd()

events = pd.read_csv('./transformed_data/combine_keystrokes.csv')
events.rename( columns={'Unnamed: 0':'unnamed_zero'}, inplace=True )
events = events.sort_values(by=['SubjectID', 'ClientTimestamp', 'unnamed_zero'], ignore_index=True)
events.to_csv(cwd + '/transformed_data' + '/filter_sort.csv', index=False)
