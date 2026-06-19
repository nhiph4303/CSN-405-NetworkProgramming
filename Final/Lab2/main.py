from app.models.node import NetworkNode
from app.config.config_manager import add_node, list_nodes, remove_node

while True:
    # 1. Hiện menu
    print("\n=== Network Node Manager ===")
    print("1. Add node")
    print("2. List nodes")
    print("3. Remove node")
    print("4. Exit")

    choice = input("Choose (1-4): ")
    
    if choice == "1":
        ip       = input("Enter IP: ")
        port     = int(input("Enter port: "))
        role     = input("Enter role (client/server): ")
        protocol = input("Enter protocol (tcp/udp): ")
        
        try:
            node = NetworkNode(ip, port, role, protocol)
            add_node(node)
            print("Node added successfully!")
        except ValueError as e:
            print("Error:", e)
    
    elif choice == "2":
        list_nodes()

    elif choice == "3":
        node_id = input("Enter node_id to remove: ")
        remove_node(node_id)
        print("Node removed!")

    elif choice == "4":
        print("Goodbye!")
        break   
    else:
        print("Invalid choice!")