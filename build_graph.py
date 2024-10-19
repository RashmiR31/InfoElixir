import streamlit as st
from neo4j import GraphDatabase
from upload_files import upload_blob
from datetime import datetime

URI = st.secrets["NEO4J_URI"]
AUTH = (st.secrets["NEO4J_USERNAME"],st.secrets["NEO4J_PASSWORD"])

driver = GraphDatabase.driver(uri=URI, auth=AUTH)

# current time
now = datetime.now()
formatted_time = now.strftime("%b %d, %Y, %I:%M:%S %p")

# Data={
#     "name":"rashmi",
#     "subject":"AI",
#     "topic":{
#         "title":"algorithm",
#         "file_path":"/Users/rashmir/Desktop/hack/Assignment_RM.pdf"
#     }
# }

def create_graph(Data):
    name = Data["name"]
    subject = Data["subject"]
    topic_title=Data["topic"]["title"]
    topic_path=Data["topic"]["file_path"]
    file_name = topic_path.split("/" or "\\")[-1]
    print(file_name)
    
    # upload the pdf to google storage
    upload_blob(file_path=topic_path,destination_blob_name=f"{name}/{file_name}")
    destination_file_path = f"https://storage.cloud.google.com/infoelixir_data/{name}/{file_name}"

    query = """
    MERGE (p:Person {name: $name})-[:READS]->(s:Subject {title: $sub_title})
    MERGE (s)-[:HAS]->(t:Topic {topic: $topic_title,file_path: $file_path,updated: $updated_time})
    """
    graph_creation = driver.execute_query(
        query_=query,
        name=name,
        sub_title=subject,
        topic_title=topic_title,
        file_path=destination_file_path,
        updated_time=formatted_time
    )

def create_initial_graph(Data):
    for k,v in Data.items():
        person_name = str(k)

        # create person node
        name_creation = driver.execute_query(
            "Merge (p:Person {name: $name})",
            name=person_name,
            database_="neo4j"
        ).summary
        print("Created {nodes_created} nodes in {time} ms.".format(
            nodes_created=name_creation.counters.nodes_created,
            time=name_creation.result_available_after
        ))
        print(person_name)
        # add subjects
        for subs,topics in Data[k].items():
            subject_addition = driver.execute_query(
                """
                Match (p:Person {name: $name})
                Merge (p)-[:READS]->(s:Subject {title: $title})
                """,
                name = person_name,
                title = subs,
                database_="neo4j"
            ).summary
            print("Created {nodes_created} nodes in {time} ms.".format(
            nodes_created=subject_addition.counters.nodes_created,
            time=subject_addition.result_available_after
            ))
            for topic in topics:
                topic_addition = driver.execute_query(
                    """
                    Match (p:Person {name: $name})-[:READS]->(s:Subject {title: $title})
                    merge (s)-[:HAS]->(t:Topic {topic: $topic, file_path: $file_path, updated: $updated_time})
                    """,
                    name=person_name,
                    title=subs,
                    topic=topic,
                    database_="neo4j"
                )

######
#merge (p:Person {name: "likith"})-[:READS]->(s:Subject {title: "AI"})
#merge (s)-[:HAS]->(t:Topic {topic: "supervised learning",file_path: "https://storage.cloud.google.com/infoelixir_data/rashmi/assignment.pdf",updated: "Oct 18, 2024, 2:21:58 PM"})

def add_subjects_to_graph(name,subject,topic):
    topic_title=topic["title"]
    topic_path= topic["file_path"]

    # upload the pdf to google storage
    file_name = topic_path.split("/" or "\\")[-1]
    upload_blob(file_path=topic_path,destination_blob_name=f"{name}/{file_name}")
    destination_file_path = f"https://storage.cloud.google.com/infoelixir_data/{name}/{file_name}"

    # first add the subject
    query = """
    MATCH (p:Person {name: $name})
    MERGE (p)-[:READS]->(s:Subject {title: $title})
    """
    add_subjects = driver.execute_query(query_=query, name=name,title=subject)
    # now add all topics under it

    query = """
    MATCH (p:Person {name: $name})-[:READS]->(s:Subject {title: $sub_title})
    MERGE (s)-[:HAS]->(t:Topic {topic: $topic_title,file_path: $file_path,updated: $updated_time})
    """
    add_topics = driver.execute_query(query_=query,name=name,sub_title=subject,topic_title=topic_title,
        file_path=destination_file_path,
        updated_time=formatted_time)

def update_topics(name,subject,topic):
    topic_title=topic["title"]
    topic_path= topic["file_path"]

    # upload the pdf to google storage
    file_name = topic_path.split("/" or "\\")[-1]
    upload_blob(file_path=topic_path,destination_blob_name=f"{name}/{file_name}")
    destination_file_path = f"https://storage.cloud.google.com/infoelixir_data/{name}/{file_name}"

    query = """
    MATCH (p:Person {name: $name})-[:READS]->(s:Subject {title: $sub_title})
    MERGE (s)-[:HAS]->(t:Topic {topic: $topic_title,file_path: $file_path,updated: $updated_time})
    """
    add_topics = driver.execute_query(query_=query,name=name,sub_title=subject,topic_title=topic_title,
        file_path=destination_file_path,
        updated_time=formatted_time)


def delete_subject(name,subject):
    query = """
    MATCH (p:Person {name: $name})-[:READS]->(s:Subject {title: $title})-[:HAS]-(t:Topic)
    DETACH DELETE s,t
    """
    delete_subject = driver.execute_query(query_=query,name = name,title=subject).summary
    


driver.close()
