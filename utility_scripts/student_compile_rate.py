import pandas as pd
import os

cwd = os.getcwd()
print(cwd)

initial_data = pd.read_csv('./transformed_data/dist_edit_to_error.csv')

initial_data['compile_int'] = initial_data.apply(lambda row: 1 if row.would_compile else 0, axis = 1)

compile_rate = (initial_data.groupby(['user_id'])
   .agg({
       'compile_int': ['mean', 'count']
    }))


compile_rate.columns = compile_rate.columns.map('_'.join)
compile_rate.to_csv('./transformed_data/student_compile_rate.csv')

