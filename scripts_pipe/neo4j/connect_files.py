import csv
import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase

def find_files(tx):
    result = tx.run("MATCH (f:File) RETURN f")
    return [record["f"] for record in result]

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
            files = session.read_transaction(find_files)

            for file in files:
                subject_id = file.get('SubjectID')
                assignment_id = file.get('AssignmentID')
                task = file.get('Task')

                session.run(f'''
                    MATCH (f:File {{
                        SubjectID: '{subject_id}',
                        AssignmentID: '{assignment_id}',
                        Task: '{task}'
                    }}
                    )
                    <-[:IN]-(e:Event)
                    WITH e
                    ORDER BY e.ClientTimestamp ASC
                    WITH collect(e) as events
                    CALL apoc.nodes.link(events, 'THEN')
                    RETURN events
                    ''')



    finally:
        driver.close()
