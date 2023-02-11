import pandas as pd
import os

cwd = os.getcwd()
print(cwd)

initial_data = pd.read_csv('./transformed_data/dist_edit_to_error.csv')

initial_data['compile_int'] = initial_data.apply(lambda row: 1 if row.would_compile else 0, axis = 1)

print('Compile rate')
print(initial_data['compile_int'].mean())

compile_rate = (initial_data.groupby(['user_id'])
   .agg({
       'compile_int': ['mean', 'count']
    }))


compile_rate.to_csv('./transformed_data/project_compile_rate.csv')

