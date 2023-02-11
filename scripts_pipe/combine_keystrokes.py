import pandas as pd
import os

print('Running script combine_keystrokes')
cwd = os.getcwd()

keystrokes_2019 = pd.read_csv(cwd + '/source_data/Keystroke Data 2019/keystrokes.csv')
keystrokes_fall_2021 = pd.read_csv(cwd + '/source_data/Keystroke Data 2021/keystrokes.csv')

keystrokes_2019['semester'] = 'fall2019'
keystrokes_fall_2021['semester'] = 'fall2021'

combined = pd.concat([keystrokes_2019, keystrokes_fall_2021], axis=0)

print(f'Combined dataframe of length {len(keystrokes_2019)} with dataframe of length {len(keystrokes_fall_2021)} to combined length of {len(combined)}')

combined.to_csv('./transformed_data/combine_keystrokes.csv')
