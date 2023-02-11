import pandas as pd
import csv
import os

cwd = os.getcwd()
print(cwd)

new_format = bool(input('Type "T" for new format, "F" for old format:\n'))

if new_format:
    print('Loading new format data')
    raw_data = pd.read_csv(cwd + '/source_data' + '/events.csv')

    # filter to just the edit events
    df_edit_events = raw_data[raw_data.type == 'e']
    print('Data loaded')

    # chose a subject
    all_subjects = df_edit_events.subject.unique()
    print('Available subjects:')
    print(all_subjects)
    selected_subject = input('Choose a subject:\n')
    print(f'Selected subject {selected_subject}')
    df_user_selected = df_edit_events[df_edit_events.subject == selected_subject]

    # chose an assignment
    assignments = df_user_selected.assnName.unique()
    print('Available assignments:')
    print(assignments)
    selected_assignment = input('Choose an assignment:\n')
    print(f'Selected assignment: {selected_assignment}')
    df_assn_selected = df_user_selected[df_user_selected.assnName == selected_assignment]

    files = df_assn_selected.file.unique()
    print('Available files: ')
    print(files)
    selected_file = input('Choose a file:\n')
    print(f'Selected file: {selected_file}')
    df_file_selected = df_assn_selected[df_assn_selected.file == selected_file]

    df_file_selected.to_csv(cwd + f'/source_data/new_format/{selected_subject}-{selected_assignment}-{selected_file}.csv', header = True, index = False, quoting=csv.QUOTE_ALL)

    print(len(df_file_selected))
    print('Success!')

else:
    print('Loading data. This may take a while.')
    raw_data = pd.read_csv(cwd + '/source_data' + '/project-events.csv')
    print('Data loaded')
    raw_data.rename( columns={'Unnamed: 0':'unnamed_zero'}, inplace=True )

    # chose a user
    all_users = raw_data.user_id.unique()
    print('Available users:')
    print(all_users)
    selected_user = input('Choose a user:\n')
    print(f'Selected user {selected_user}')
    df_user_selected = raw_data[raw_data.user_id.isin([int(selected_user)])]

    # chose the project
    all_projects = df_user_selected.project_id.unique()
    print('Available projects:')
    print(all_projects)
    selected_project = input('Choose a project:\n')
    print(f'Selected project {selected_project}')
    df_project_selected = df_user_selected[df_user_selected.project_id.isin([int(selected_project)])]

    # chose the task
    all_tasks = df_project_selected.task.unique()
    print('Available tasks:')
    print(all_tasks)
    selected_task = input('Choose a task:\n')
    print(f'Selected task {selected_task}')
    df_task_selected = df_project_selected[df_project_selected.task.isin([int(selected_task)])]

    df = df_task_selected.sort_values(by=['timestamp', 'unnamed_zero'])
    print(len(df))

    df.to_csv(cwd + '/source_data/long_recoveries/' + str(selected_user) + '-' + str(selected_project) + '-' + str(selected_task) + '.csv', header = True, index = False, quoting=csv.QUOTE_ALL)
