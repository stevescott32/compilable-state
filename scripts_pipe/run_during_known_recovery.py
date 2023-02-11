import csv
import sys

# some events have very large fields, increase limit
csv.field_size_limit(sys.maxsize)

print('Running script run before recovery')

one_known_recovery_results = []

current_subject = ''
current_assignment = ''
current_file = ''
current_task = ''

recovery_left = 0
in_known_recovery = False
in_recovery = False
run_before_recovery_known = False
run_before_recovery_unknown = False

user_count = 0

with open('transformed_data/sort_task.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    with open('transformed_data/run_before_recovery.csv', 'w', newline='')  as output_file:

        current_row = next(reader)

        current_row['run_before_recovery_known'] = False # tmp for headers
        current_row['run_before_recovery_unknown'] = False # tmp for headers
        current_row['known_recovery_start'] = False # tmp for headers
        current_row['recovery_start'] = False # tmp for headers
        dict_writer = csv.DictWriter(output_file, current_row.keys())
        dict_writer.writeheader()

        while current_row:

            while ( current_row and \
                current_row['SubjectID'] == current_subject \
                and current_row['AssignmentID'] == current_assignment \
                and current_row['CodeStateSection'] == current_file \
                and current_row['X-Task'] == current_task) \
                :

                if current_row['would_compile'] == 'True':
                    if len(one_known_recovery_results) > 0:
                        if in_known_recovery:
                            one_known_recovery_results[0]['run_before_recovery_known'] = run_before_recovery_known
                        elif in_recovery:
                            one_known_recovery_results[0]['run_before_recovery_unknown'] = run_before_recovery_unknown
                    dict_writer.writerows(one_known_recovery_results)
                    one_known_recovery_results = []
 
                    in_known_recovery = False
                    in_recovery = False
                    run_before_recovery_known = False
                    run_before_recovery_unknown = False

                if current_row['switch_to_fail'] == 'True':
                    in_recovery = True
                    current_row['recovery_start'] = True
                else:
                    current_row['recovery_start'] = False

                if current_row['EventType'] == 'Run.Program' and current_row['would_compile'] == 'False':
                    if in_known_recovery:
                        run_before_recovery_known = True
                    if in_recovery:
                        run_before_recovery_unknown = True


                if current_row['last_run_would_compile'] == 'True' and current_row['would_compile'] == 'False' and current_row['EventType'] == 'Run.Program':
                    current_row['known_recovery_start'] = True
                    in_known_recovery = True
                    if len(one_known_recovery_results) > 0:
                        one_known_recovery_results[0]['run_before_recovery_unknown'] = run_before_recovery_unknown
                    dict_writer.writerows(one_known_recovery_results)
                    one_known_recovery_results = []
                else:
                    current_row['known_recovery_start'] = False

                one_known_recovery_results.append(current_row)
                current_row = next(reader, None)


            dict_writer.writerows(one_known_recovery_results)
            one_known_recovery_results = []

            # set up for the next iteration
            current_subject = current_row['SubjectID'] if current_row else ''
            current_assignment = current_row['AssignmentID'] if current_row else ''
            current_file = current_row['CodeStateSection'] if current_row else ''
            current_task = current_row['X-Task'] if current_row else ''
