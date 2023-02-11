# Script Order, Purposes, and Assumptions

All scripts output a csv of their same name

- Filter Sort
  - Purpose: group the events by (user_id, project_id, task), then sort them by timestamp + unnamed zero
  - Requires:
    - project_events.csv

- Compile Every Event
  - Determine if the student's file would compile after each event
  - Columns added:
    - would_compile
    - error_message

- Error Line 
  - Requires:
    - error_message from Compile Every Event
  - Columns added:
    - error_line

- Orig Error Line
  - Requires:
    - error_message from Compile Every Event
    - error_line from Error Line
