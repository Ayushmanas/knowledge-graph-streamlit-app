from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pyvis.network import Network
import asyncio



#Load the env variable
load_dotenv()
# Get API key from env variable
api_key = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(temperature=0, model_name='gpt-4o')
graph_transformer = LLMGraphTransformer(llm=llm)

#Extract graph data from input text
async def extract_graph_data(text):
    """
    Generates graph documents based on provided text
    Args:
        text (str): textual data or document needed to be converted to graph document
    Returns:
        list: A list of graph document objects containing nodes and relationships.
    """
    
    docuemnts = [Document(page_content=text)]
    graph_documents = await graph_transformer.aconvert_to_graph_documents(documents=docuemnts)
    return graph_documents

#Visualize the knowledge graph
def visualize_graph(graph_documents):
    # Create a network
    network = Network(height="1200px",width='100%', directed=True,
                      notebook=False, bgcolor="#222223", font_color="white")
    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships
    
    #Build lookup for valid nodes
    node_dict = {node.id: node for node in nodes}
    
    #Filter out invalid edges and collect valid node ids
    valid_edges = []
    valid_node_ids = set()
    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])
    
    #Track which nodes are part of any relationship
    connected_node_ids = set()
    for rel in relationships:
        connected_node_ids.add(rel.source.id)
        connected_node_ids.add(rel.target.id)
    
    #Add valid nodes to the network
    for node_id in valid_node_ids:
        node = node_dict[node_id]
        try:
            network.add_node(node.id, label=node.id, title=node.type, group=node.type)
        except:
            continue #skip if error encountered
    
    #Add valid edges to the network
    for rel in valid_edges:
        try:
            network.add_edge(rel.source.id, rel.target.id, label=rel.type.lower())
        except:
            continue #skip if error encountered
    
    #Configure physics
    network.set_options("""
            {
                "physics": {
                    "forceAtlas2Based": {
                        "gravitationalConstant": -100,
                        "centralGravity": 0.01,
                        "springLength": 200,
                        "springConstant": 0.08
                    },
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }
            """)
    output_file = "knowledge_graph.html"
    #Save the graph
    try:
        network.save_graph(output_file)
        print("Graph saved to:",os.path.abspath(output_file))
        return network
    except Exception as e:
        print(f'Error {e} encountered while saving knowledge graph!')
        return None
    
    # # Try to open in browser:
    # try:
    #     import webbrowser
    #     webbrowser.open(f"file://{os.path.abspath(output_file)}")
    #     return net
    # except:
    #     print('Could not open browser automatically')

# Visualize the knowledge graph after extraction
def generate_knowledge_graph(text):
    """Generates and visualizes a knowledge graph from input text
    
    This function runs the graph extraction asynchronously and then visualizes
    the resulting graph using Pyvis.

    Args:
        text (string): input text to convert to knowledge graph

    Returns:
        pyvis.network.Network: The visualized network graph object
    """
    graph_documents = asyncio.run(extract_graph_data(text))
    net = visualize_graph(graph_documents)
    return net
