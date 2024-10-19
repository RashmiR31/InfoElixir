from openai import OpenAI
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

def chat_bot():
    st.title("💬 InfoElixir")
    st.caption("🚀 A Streamlit chatbot powered by OpenAI")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        graph = Neo4jGraph(
        url=st.secrets["NEO4J_URI"],
        username="neo4j",
        password=st.secrets["NEO4J_PASSWORD"]
        )

        def run_query(query):
            with neo4j_driver.session() as session:
                result = session.run(query)
                return [record.data() for record in result]
            

        template="""
        You are a helpful bot who tells information from the knowledge graph by generating accurate cypher queries to query the neo4j graph database.
        The knowledge graph consists of 3 majorly labelled nodes.
        1. Person : contains name of the person all in lowercase
        2. Subject: contains title of subject
        3. Topic: contains topic and file_path of the topic
        There are 2 relationships defined: READS and HAS
        Basic structure looks like this,
        (p:Person)-[:READS]->(s:Subject)-[:HAS]->(t:Topic)
        A Person can read many subjects and a subject can have many topics.

        Translate this query to cypher: {prompt}
        """
        template = PromptTemplate(
            input_variables=["natural_language_query"],
            template=template
        )

        chain = LLMChain(llm=llm, prompt=template)
        cypher_query = chain.run(prompt)
        print(cypher_query)
        results = run_query(cypher_query)

        if results:
            print(results)
            # results_str = "\n".join([
            #     f"Person: {record.get('p', {}).get('name', 'Unknown')}, Subject: {record.get('s', {}).get('title', 'Unknown')}, Topic: {record.get('t', {}).get('title', 'Unknown')}" 
            #     for record in results
            # ])
            
            natural_language_template = """
            The result is in json format extracted from knowledge graph of structure (p:Person)-[:READS]->(s:Subject)-[:HAS]->(t:Topic). 
            Tell result in casual and simple words. No need to explain relationships. organize the output.
            Query given was: {query_given}


            
            
            {results_str}
            """
            natural_language_template = PromptTemplate(
                input_variables=["results_str","query_given"],
                template=natural_language_template
            )

            # Create the second chain for generating natural language response
            inputs = {
                "results_str": results,
                "query_given": cypher_query
            }
            natural_language_chain = LLMChain(llm=llm, prompt=natural_language_template)
            natural_language_response = natural_language_chain.run(inputs)
        else:
            natural_language_response = "I couldn't find any information related to your query."

        st.session_state.messages.append({"role": "assistant", "content": natural_language_response})
        st.chat_message("assistant").write(natural_language_response)

    # print(results)
    # msg = results
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg)