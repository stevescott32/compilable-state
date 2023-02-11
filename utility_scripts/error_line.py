from numpy.lib.shape_base import split
import pandas as pd
import os

cwd = os.getcwd()
print(cwd)

df = pd.read_csv(cwd + '/transformed_data/compile_every_event.csv')

def find_line_number(error_message):
    if error_message == '' or not type(error_message) == str:
        return ''
    split_message = error_message.split()
    if 'line' in split_message:
        # find the index of the last occurance of the word "line" + 1 (implicit) to find where the line number is
        # line_number_index = split_message.index('line') + 1
        line_number_index = len(split_message) - split_message[::-1].index('line')
        uncleaned_line_number = split_message[line_number_index]
        line_number = ''.join(c for c in uncleaned_line_number if c.isdigit())
        return line_number
    return 0


df['error_line'] = df['error_message'].apply(find_line_number)

df.to_csv(cwd + '/transformed_data/error_line.csv')
