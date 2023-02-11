'''
The purpose of this script is to track which lines error originated from in order
to get a better sense of how long it takes the user to fix a particular error.
'''

import csv
import os
import sys
import uuid

class SyntaxError:
    original_error_line = -1
    error_message = ''
    current_error_line = -1
    num_occurances = 1

    def __init__(self):
        self.id = uuid.uuid4()

    def get_message_sans_num(self):
        message_sans_num = ''.join(c for c in self.error_message if not c.isdigit())
        return message_sans_num

    def has_same_message(self, other_syntax_error):
        return other_syntax_error.get_message_sans_num() == self.get_message_sans_num()

    def get_offset(self):
        return self.current_error_line - self.original_error_line

    def to_json(self):
        return f'{{ "error_message": "{self.error_message}", "current_error_line": "{self.current_error_line}", "num_occurances": "{self.num_occurances}", "id": "{self.id}", "original_error_line": "{self.original_error_line}" }}'


cwd = os.getcwd()
print(cwd)

csv.field_size_limit(sys.maxsize)

print('Loading data')
data_path = cwd + '/transformed_data' + '/error_line.csv'

results = []
stack = []

curr_user_id = ''
curr_project_id = '0'
curr_task = '0'

i = 0
offset = 0

with open(data_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if(not (row['user_id'] == curr_user_id and row['project_id'] == curr_project_id and row['task'] == curr_task)):
            curr_user_id = row['user_id']
            curr_project_id = row['project_id']
            curr_task = row['task']
            stack = []
        if row['would_compile'] == 'True':
            stack = []
        if row['error_line'] == '' or row['would_compile'] == 'True':
            row['original_error_line'] = ''
            row['curr_error_id'] = ''
            row['curr_errors'] = '[]'
        else:
            try:
                add_as_new = True
                current_error_line = int(float(row['error_line']))
                current_syntax_error = SyntaxError()
                current_syntax_error.original_error_line = current_error_line
                current_syntax_error.current_error_line = current_syntax_error.original_error_line
                current_syntax_error.error_message = row['error_message']

                code_added_length = len(row['code_added'].split()) - 1
                code_removed_length = len(row['code_removed'].split()) - 1
                # if no lines were added/removed, one of these lengths will be -1. Change to be zero
                code_added_length = code_added_length if code_added_length > 0 else 0 # change negative values to zero
                code_removed_length = code_removed_length if code_removed_length > 0 else 0 # change negative values to zero
                for s in stack:
                    if current_error_line < s.current_error_line:
                        s.current_error_line -= code_removed_length
                        s.current_error_line += code_added_length

                # filter the list of syntax errors to the ones that appear on later lines than the current error
                # assumption: if the current error is on a later line than a previous error, the previous error is fixed
                stack = [x for x in filter(lambda e: e.current_error_line >= current_syntax_error.current_error_line, stack)]

                for s in stack:
                    # check if any of the syntax errors match, indicating the new error doesn't need to be added to the stack
                    if current_syntax_error.has_same_message(s) and current_syntax_error.current_error_line == s.current_error_line:
                        add_as_new = False
                        row['curr_error_id'] = s.id
                        row['original_error_line'] = s.original_error_line
                    s.num_occurances = s.num_occurances + 1
                
                if add_as_new:
                    stack.append(current_syntax_error)
                    row['original_error_line'] = current_syntax_error.original_error_line
                    row['curr_error_id'] = current_syntax_error.id
                row['curr_errors'] = '[' + ','.join(e.to_json() for e in stack) + ']'
            except BaseException as e:
                print(i)
                print(row)
                raise e
            
        results.append(row)

        # progress tracking
        i += 1
        if i % 10000 == 0:
            print(i)
            pass


keys = results[0].keys()
with open('transformed_data/orig_error_line.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
