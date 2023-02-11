import pandas as pd
import os

exam_sum_column = 'ExamSum'
exam_average_column = 'ExamAverage'

print('Running script combine_students')
cwd = os.getcwd()

students_2019 = pd.read_csv(cwd + '/source_data/Keystroke Data 2019/students.csv')

# add in exam aggregation stats for 2 exam semesters
students_2019[exam_sum_column] = students_2019.exam1 + students_2019.exam2
students_2019[exam_average_column] = students_2019[['exam1', 'exam2']].mean(axis=1)

students_fall_2021 = pd.read_csv(cwd + '/source_data/Keystroke Data 2021/students.csv')

# add in exam aggregation stats for 3 exam semesters
students_fall_2021[exam_sum_column] = students_fall_2021.Exam1 + students_fall_2021.Exam2 + students_fall_2021.Exam3
students_fall_2021[exam_average_column] = students_fall_2021[['Exam1', 'Exam2', 'Exam3']].mean(axis=1)

students_2019['semester'] = 'fall2019'
students_fall_2021['semester'] = 'fall2021'

combined = pd.concat([students_2019, students_fall_2021], axis=0).reset_index()

print(f'Combined dataframe of length {len(students_2019)} with dataframe of length {len(students_fall_2021)} to combined length of {len(combined)}')

combined.to_csv('./transformed_data/combine_students.csv')
