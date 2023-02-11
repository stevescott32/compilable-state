echo "Running data pipe"
# Combine data for keystrokes of different semesters
time python ./scripts_pipe/combine_keystrokes.py
# Combine data for grades of different semesters
time python ./scripts_pipe/combine_students.py
# Filter and sort the combined keystroke data
time python ./scripts_pipe/filter_sort.py
# Attempt to compile every event
time python ./scripts_pipe/compile_every_event.py
# track switches from compile success to compile failure and vice versa
time python ./scripts_pipe/switches.py
# sort so that all events in a file are together
time python ./scripts_pipe/sort_file.py
# add column for whether the last run would compile
time python ./scripts_pipe/last_run_would_compile.py
# categorize when in recovery
time python ./scripts_pipe/in_known_recovery.py
# switch to task sorting
time python ./scripts_pipe/sort_task.py
# count how many events are between the current event and the next event that would compile
time python ./scripts_pipe/recovery_left.py
# count how many events until the next run
time python ./scripts_pipe/n_to_next_run.py
# count how many events until the next successful run
time python ./scripts_pipe/n_to_successful_run.py
# capture what the next event type is for filtering
time python ./scripts_pipe/next_event_type.py
# calculate where each event is within its task
time python ./scripts_pipe/place_in_task.py
# determine recovery starts and whether runs occur within recoveries
time python ./scripts_pipe/run_during_known_recovery.py
# copy last result so notebooks can expect a consistent location
cp ./transformed_data/run_during_known_recovery.csv ./transformed_data/pipe_results.csv
# create a shortened version of the result so it can be more easily opened
head -n 10000 ./transformed_data/pipe_results.csv > ./transformed_data/pipe_results.small.csv
