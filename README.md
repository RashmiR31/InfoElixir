#  **InfoElixir**

## **Theme: Improving Work Efficiency**

### **Problem Statement: Knowledge Distiller App**

## Demo Video: 
https://drive.google.com/file/d/1q4h93_UQHyEgCYlvc470GEKdgGrYfoQu/view?usp=sharing

## **Introduction**
- InfoElixir is designed to streamline study material organization and retrieval.
- The app supports multiple input formats: text, images, handwritten notes, and audio.
- It automatically parses and extracts meaningful data from these formats.
- A personalized knowledge graph connects key concepts for better study efficiency.
- The chatbot enables quick information retrieval based on individual study needs.

## **Approach**

1. **User Authentication**:  
   Users can log in or register to access their personalized dashboard.
   
2. **Dashboard & File Upload**:  
   Users upload study materials which dynamically update their personal knowledge graph.
   
3. **Knowledge Graph**:  
   Neo4j graph database is integrated via its API to create and visualize knowledge graphs.
   
4. **Chatbot Integration**:  
   A chatbot powered by OpenAI and backed by Neo4j's API retrieves relevant information from the knowledge graph.
   
5. **Collaborative Features**:  
   Users can plot and view graphs of their friends, fostering a collaborative learning environment.

## **Tech Stack**

### **Backend-API**
- MySQL
- Flask
- Flask-RESTx

### **Frontend**
- Streamlit

### **Chatbot**
- Streamlit
- OpenAI

### **Graph Database**
- Neo4j: **Retrieval augmented generation based on the Neo4j knowledge graph**

## **System Architecture Diagram**
![image](https://github.com/user-attachments/assets/58de9d74-720a-48fd-85ea-ef40f3bcbf83)


**Sample Knowledge Graph**
![c9530b65-3d29-4744-adce-6db35de3620f](https://github.com/user-attachments/assets/dab86ac2-f70b-462f-9639-541b2a774993)

## **Conclusion**
our app offers an innovative solution to enhance students’ learning efficiency by organizing study materials and connecting key concepts through personalized knowledge graphs. With multi-format input support and seamless information retrieval via an intelligent chatbot, the app provides a tailored and collaborative study experience.

## Screenshots
<img width="802" alt="Screenshot 2024-10-19 at 8 18 23 PM" src="https://github.com/user-attachments/assets/da7251d3-f6d2-4b8e-8747-cba8988f4da8">
<br>
<img width="678" alt="Screenshot 2024-10-19 at 8 20 09 PM" src="https://github.com/user-attachments/assets/bf63e0bd-81af-4760-8c96-67013bf06a02">
<br>
<img width="964" alt="Screenshot 2024-10-19 at 8 21 37 PM" src="https://github.com/user-attachments/assets/eda183b0-7e14-453a-b53e-2701b89a4d78">
<br>
<h3>Knowledge graph</h3>
<img width="536" alt="Screenshot 2024-10-19 at 8 22 18 PM" src="https://github.com/user-attachments/assets/731cf5b4-a5b8-4941-97f3-0d57b2b80e0c">
<br>
<h3>Retrieval Augmented Generation</h3>
<img width="742" alt="Screenshot 2024-10-19 at 8 23 47 PM" src="https://github.com/user-attachments/assets/9c06dddb-2b29-4918-9789-a0f083d5da93">
<img width="661" alt="Screenshot 2024-10-19 at 8 24 35 PM" src="https://github.com/user-attachments/assets/e37383cf-0bad-4d3b-bba8-e70aadbb630b">
<img width="673" alt="Screenshot 2024-10-19 at 8 25 46 PM" src="https://github.com/user-attachments/assets/d7db9f92-9717-4186-aac6-4c380770b24f">





