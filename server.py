import socket          # Importing the socket module for network communication
import ipaddress       # Importing to validate IP addresses

def tcp_server():
    # Ask for server IP to bind to
    localIP = input("What is the IP address? ") 
    
    # Validate if the IP is either IPv4 or IPv6
    try:
        ipaddress.ip_address(localIP)
    except ValueError:
        print("Invalid IP address.")
        return
    
    # Ask for the port
    port = int(input("What is the Port number of server? "))  
    
    # Check if the port is in the valid range
    if not (0 < port <= 65535):                         
        raise ValueError("Port number must be between 1 and 65535")

    # Start the TCP socket for communication between server and client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind the socket to the local IP and port
        server_socket.bind(('0.0.0.0', port))
    except socket.error as err:
        print(f"Socket binding error: {err}")
        return
    
    # Start listening for connections
    print(f"Waiting for client on {localIP}:{port}...")                      
    server_socket.listen(5)                             # Listen for connections, with a queue size of 5 clients

    while True:
        # Accept the connection from a client
        incoming_socket, incoming_address = server_socket.accept()
        print(f"Connection from {incoming_address}")

        while True:
            try:
                # Receive message from the client (1024 bytes max), then decode
                message = incoming_socket.recv(1024).decode().strip()

                # If the message is empty or client sends 'exit', break the loop and close connection
                if len(message) == 0 or message.lower() == 'exit':
                    print(f"Client {incoming_address} disconnected.")
                    break

                print(f"Message received from client: {message}")
                
                # Send the uppercase version of the received message back to the client
                incoming_socket.send(message.upper().encode())

            except ConnectionResetError:
                print(f"Connection with {incoming_address} was reset.")
                break
        
        # Close the connection after the loop ends
        incoming_socket.close()
        print(f"Connection closed with {incoming_address}.")
        break
        

    # Close the server socket when the server is terminated
    server_socket.close()

if __name__ == "__main__":
    tcp_server()
