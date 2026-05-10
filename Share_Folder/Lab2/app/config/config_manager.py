import json
import os
from app.models.node import NetworkNode

FILE_PATH = "data/nodes.json"

def load_nodes() -> list:
    if not os.path.exists(FILE_PATH) or os.stat(FILE_PATH).st_size == 0:
        return []
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_nodes(nodes: list):
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    with open(FILE_PATH, "w") as file:
        json.dump(nodes, file, indent=4)

def add_node(ip: str, port: int, role: str, protocol: str):
    try:
        new_node = NetworkNode(ip, port, role, protocol)
        nodes = load_nodes()
        nodes.append(new_node.to_dict())
        save_nodes(nodes)
        print("Node added.")
    except Exception as e:
        print(f"Error adding node: {e}")

def remove_node(node_id: str):
    nodes = load_nodes()
    original_count = len(nodes)
    
    nodes = [node for node in nodes if node.get("node_id") != node_id]
    
    if len(nodes) < original_count:
        save_nodes(nodes)
        print("Node removed.")
    else:
        print("Node not found.")

def list_nodes():
    nodes = load_nodes()
    if not nodes:
        print("List nodes is empty.")
        return
        
    print(f"{'ID':<38} | {'IP':<15} | {'Port':<6} | {'Role':<6} | {'Protocol'}")
    print("-" * 85)
    for node in nodes:
        print(f"{node['node_id']:<38} | {node['ip']:<15} | {node['port']:<6} | {node['role']:<6} | {node['protocol']}")