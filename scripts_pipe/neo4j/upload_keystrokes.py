import csv
import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)
    print(f'cwd: {os.getcwd()}')
    # get neo4j connection information from the env
    load_dotenv()
    uri = "bolt://localhost:7687"
    password = os.environ.get('NEO4J_PASSWORD')
    user = os.environ.get('NEO4J_USER')
    database = os.environ.get('NEO4J_DATABASE')

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))

        with driver.session() as session:
            with open('transformed_data/pipe_results.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                current_subject = ''
                current_assignment = ''
                current_file = ''
                current_task = ''

                one_file_results = []
                current_row = next(reader)

                while current_row:

                    while ( current_row and \
                        current_row['SubjectID'] == current_subject \
                        and current_row['AssignmentID'] == current_assignment \
                        and current_row['CodeStateSection'] == current_file \
                        and current_row['X-Task'] == current_task) \
                        :

                        one_file_results.append(current_row)
                        current_row = next(reader, None)
                
                    if len(one_file_results) > 0:
                        # upload this file to neo4j
                        result = session.run('''
                            CREATE (f:File {
                                SubjectID: $file.SubjectID,
                                AssignmentID: $file.AssignmentID,
                                CodeStateSelection: $file.CodeStateSelection,
                                Task: $file.`X-Task`
                                }
                            )
                            WITH f
                            UNWIND $events AS event
                                CREATE (f)<-[:IN]-(e:Event {
                                    EventId: event.EventID,
                                    SubjectID: event.SubjectID,
                                    AssignmentID: event.AssignmentID,
                                    CodeStateSection: event.CodeStateSection,
                                    Task: event.`X-Task`,
                                    EventType: event.EventType,
                                    Keystroke: event.`X-Keystroke`,
                                    InsertText: event.InsertText,
                                    DeleteText: event.DeleteText,
                                    SourceLocation: event.SourceLocation,
                                    ClientTimestamp: event.ClientTimestamp,
                                    EditType: event.EditType,
                                    RunInput: event.`X-RunInput`,
                                    RunOutput: event.`X-RunOutput`,
                                    RunHasError: event.`X-RunHasError`,
                                    RunUserTerminated: event.`X-RunUserTerminated`,
                                    RawAssignmentID: event.`X-RawAssignmentID`,
                                    Term: event.`X-Term`,
                                    Semester: event.semester,
                                    Metadata: event.`X-Metadata`,
                                    ToolInstances: event.ToolInstances,
                                    CodeStateID: event.CodeStateID,
                                    WouldCompile: event.would_compile,
                                    ErrorMessage: event.error_message,
                                    SwitchToSuccess: event.switch_to_success,
                                    SwitchToFail: event.switch_to_fail,
                                    LastRunWouldCompile: event.last_run_would_compile,
                                    InKnownRecovery: event.in_known_recovery,
                                    RecoveryLeft: event.recovery_left,
                                    CountToNextRun: event.n_to_next_run,
                                    CountToNextSuccessfulRun: event.n_to_successful_run
                                })
                            ''', 
                            { 'file': one_file_results[0], 'events': one_file_results})
                        # reset for the next run
                        one_file_results = []

                    # set up for the next iteration
                    current_subject = current_row['SubjectID'] if current_row else ''
                    current_assignment = current_row['AssignmentID'] if current_row else ''
                    current_file = current_row['CodeStateSection'] if current_row else ''
                    current_task = current_row['X-Task'] if current_row else ''


    finally:
        driver.close()
