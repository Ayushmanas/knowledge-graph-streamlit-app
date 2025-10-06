#Streamlit application as UI for our knowledge graph
#Import necessary modules
import streamlit as st
import streamlit.components.v1 as components
import os
from generate_knowledge_graph import generate_knowledge_graph

# Setup streamlit page configuration
st.set_page_config(
    page_icon=None,
    layout="wide", #Use wide layout for better graph display
    initial_sidebar_state="auto",
    menu_items=None
)

#Set the title of our app
st.title("Knowledge graph from text")

#Sidebar section for user input method (on the left side)
st.sidebar.title("Input your document")
input_method = st.sidebar.radio(
    label="Choose an input method:",
    options=["Upload txt", "Input text"], #Radio for uploading a file or manually inputting text
)

# If user chooses to upload a txt file
if input_method=='Upload txt':
    #File uploader widget in sidebar
    uploaded_file = st.sidebar.file_uploader(label="Upload txt file",type=["txt"])
    
    if uploaded_file is not None:
        # Read the uploaded file content and decode it as UTF-8 text
        text = uploaded_file.read().decode("utf-8")
        
        #Button to generate the knowledge graph
        if st.sidebar.button("Generate knowledge graph"):
            with st.spinner("Generating knowledge graph ..."):
                # Call knowledge graph function to generate the graph from text
                network = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")
                
                # Save this graph to an html file
                output_file = "knowledge_graph_temp.html"
                network.save_graph(output_file)
                
                #Open the html file and display it within the streamlit app
                HTMLFile = open(output_file, 'r', encoding='utf-8')
                components.html(HTMLFile.read(), height=1000)
else:
    #User chooses to directly input text
    text = st.sidebar.text_area("Input text", height=300)
    
    if text is not None: #Check if the text area is not empty
        if st.sidebar.button("Generate knowledge graph"):
            with st.spinner("Generating knowledge graph ..."):
                # Call knowledge graph function to generate the graph from the input text
                network = generate_knowledge_graph(text)
                st.success("Knowledge graph generated successfully!")
                
                # Save this graph to an html file
                output_file = "knowledge_graph_temp.html"
                network.save_graph(output_file)
                
                #Open the html file and display it within the streamlit app
                HTMLFile = open(output_file, 'r', encoding='utf-8')
                components.html(HTMLFile.read(), height=1000)
        