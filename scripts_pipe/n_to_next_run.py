import csv
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

print('Running script n to next run')

rev_results = []
one_file_results = []

current_subject = ''
current_assignment = ''
current_file = ''
current_task = ''

recovery_left = 0

user_count = 0

with open('transformed_data/recovery_left.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('transformed_data/n_to_next_run.csv', 'w', newline='')  as output_file:

        current_row = next(reader)

        current_row['n_to_next_run'] = 0 #tmp to have keys for header
        dict_writer = csv.DictWriter(output_file, current_row.keys())
        dict_writer.writeheader()

        while current_row:

            while ( current_row and \
                current_row['SubjectID'] == current_subject \
                and current_row['AssignmentID'] == current_assignment \
                and current_row['CodeStateSection'] == current_file \
                and current_row['X-Task'] == current_task) \
                :

                one_file_results.append(current_row)
                current_row = next(reader, None)
                
            # figure out results for this user + assn + file
            n_to_next_run = 0
            for row in reversed(one_file_results):
                n_to_next_run += 1

                row['n_to_next_run'] = n_to_next_run
                rev_results.append(row)
                if row['EventType'] == 'Run.Program':
                    n_to_next_run = 0


            # write results for this user + assn + file to disk
            dict_writer.writerows(reversed(rev_results))
            one_file_results = []
            rev_results = []

            # set up for the next iteration
            current_subject = current_row['SubjectID'] if current_row else ''
            current_assignment = current_row['AssignmentID'] if current_row else ''
            current_file = current_row['CodeStateSection'] if current_row else ''
            current_task = current_row['X-Task'] if current_row else ''
