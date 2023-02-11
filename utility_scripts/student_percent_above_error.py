import pandas as pd
import os

cwd = os.getcwd()
print(cwd)

initial_data = pd.read_csv('./transformed_data/dist_edit_to_error.csv')

initial_data['edit_above_or_at_error'] = initial_data.apply(lambda row: row.dist_edit_to_error <= 0, axis = 1)

initial_data['edit_above_or_at_error_int'] = initial_data.apply(lambda row: 1 if row.edit_above_or_at_error else 0, axis = 1)

would_not_compile = initial_data[~initial_data['would_compile']]
percentage_above_error = (would_not_compile.groupby(['user_id'])
   .agg({
       'edit_above_or_at_error_int': ['mean', 'count']
    }))


percentage_above_error.columns = percentage_above_error.columns.map('_'.join)
percentage_above_error.to_csv('./transformed_data/student_percent_above_error.csv')
