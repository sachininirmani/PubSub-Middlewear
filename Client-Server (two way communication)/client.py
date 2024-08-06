import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received: {message}")
        except ConnectionResetError:
            print("Server forcibly closed the connection.")
            client_socket.close()
            break


def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Enter message: ")
        client_socket.send(message.encode())
        if message.lower() == 'terminate':
            print("Disconnection requested from server.")
            client_socket.close()
            break


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <SERVER_PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    start_client(server_ip, server_port)
