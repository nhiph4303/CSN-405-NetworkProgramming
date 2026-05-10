import json
import os

FILE_PATH = "data/nodes.json"

#Add nodes
def load_nodes():
    if not os.path.exists(FILE_PATH):
        return [] 
    with open(FILE_PATH, "r") as f:
        return json.load(f) # lấy dữ liệu từ file

def save_nodes(nodes):
    with open(FILE_PATH, "w") as f:
        json.dump(nodes, f, indent=5)  # ghi dữ liệu vào file

def add_node(node):
    nodes = load_nodes()
    nodes.append(vars(node))  # vars() chuyển object → dict
    save_nodes(nodes)

#Delete nodes by node_id
def remove_node(node_id):
    nodes = load_nodes()  
    
    new_nodes = []      
    for n in nodes:          
        if n["node_id"] != node_id:  # Nếu KHÔNG phải node cần xóa
            new_nodes.append(n)      # thì giữ lại
    
    save_nodes(new_nodes)      


#Display the list of nodes
def list_nodes():
    nodes = load_nodes()
    if not nodes:
        print("No nodes found.")
    for node in nodes:
        print(node)
