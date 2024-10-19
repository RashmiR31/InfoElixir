import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from neo4j import GraphDatabase
from langchain_community.graphs import Neo4jGraph

# Initialize OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

NEO4J_URI = st.secrets["NEO4J_URI"]
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = st.secrets["NEO4J_PASSWORD"]

llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

URI = NEO4J_URI
AUTH = (NEO4J_USERNAME,NEO4J_PASSWORD)

neo4j_driver = GraphDatabase.driver(URI,auth=AUTH)

graph = Neo4jGraph(
    url=URI,
    username="neo4j",
    password=st.secrets["NEO4J_PASSWORD"]
)

# Define a function to execute Cypher queries
def run_query(query):
    with neo4j_driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

## briefing
template="""
You are a helpful bot who tells information from the knowledge graph by generating accurate cypher queries to query the neo4j graph database.
The knowledge graph consists of 3 majorly labelled nodes.
1. Person : contains name of the person
2. Subject: contains title of subject
3. Topic: contains title and file path of the topic
There are 2 relationships defined: READS and HAS
Basic structure looks like this,
(p:Person)-[:READS]->(s:Subject)-[:HAS]->(t:Topic)
A Person can read many subjects and a subject can have many topics.

Translate this query to cypher: {natural_language_query}
"""

# Create a LangChain prompt for generating Cypher queries
template = PromptTemplate(
    input_variables=["natural_language_query"],
    template=template
)

chain = LLMChain(llm=llm, prompt=template)

# Example usage
natural_language_query = "I am shreyan, what are the subjects  I have in my database?"
cypher_query = chain.run(natural_language_query)

# Execute the generated Cypher query
results = run_query(cypher_query)


print("Generated Cypher Query:", cypher_query)
print("Results:", results)