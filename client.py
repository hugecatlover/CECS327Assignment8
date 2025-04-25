import socket  # importing the socket module to create a network socket(highway for sending)
import ipaddress  # for checkin ip, i will be importing ipaddress in order to use a function for validating IP addresses(https://docs.python.org/3/library/ipaddress.html)


def tcp_client():
    # we will ask for server ip so that we can connect out client with the socket
    serverIP = input("What is the IP address of the server? ")

    # so, here i use the module for verifying the ip if its IPv4 or IPv6, if n
    # ipaddress.ip_address(serverIP)

    # we will ask for a port
    serverPort = int(input("What is the Port number of server? "))

    # However, we will check if it is on the range on the existing actual ports  of 65,535 possible port numbers
    if not (0 < serverPort <= 65535):
        raise ValueError("Port number must be between 1 and 65535")

    # Start the TCP socket for communication between server and client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # now, we connect the client to the serverIP address and port given
    client_socket.connect((serverIP, serverPort))

    # Start communication with server, ask for a message to send to server to capitalize
    message = input("What is the message you want to send? ")
    while (
        len(message) != 0
    ):  # Continue sending messages until the user inputs an empty string
        client_socket.send(
            message.encode()
        )  # Sending the message to the server, encoded as bytes
        print("Sending message to server...")  # Notify when message is being sent

        # the server recieves the response
        server_response = client_socket.recv(
            1024
        ).decode()  # Receive the response from the server and decode it
        print(
            f"Message from server: {server_response}"
        )  # Print the server's response which would be capital letter message

        # Ask for another message, or an empty input to stop sending
        message = input(
            "What is another message you want to send? (enter nothing if you don't want to send anymore) "
        )

    # Close the connection with server when done
    client_socket.close()


if __name__ == "__main__":
    tcp_client()
