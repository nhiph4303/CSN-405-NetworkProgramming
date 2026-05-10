from app.config.config_manager import add_node, list_nodes, remove_node

def main():
    while True:
        print("\n1. Add node")
        print("2. List nodes")
        print("3. Remove node")
        print("4. Exit")
        
        choice = input("Option: ")
        
        if choice == '1':
            ip = input("IP: ")
            port = input("Port: ")
            role = input("Role (client/server): ")
            protocol = input("Protocol (tcp/udp): ")
            
            add_node(ip, port, role, protocol)
            
        elif choice == '2':
            list_nodes()
            
        elif choice == '3':
            node_id = input("Enter node_id to remove: ")
            remove_node(node_id)
            
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()