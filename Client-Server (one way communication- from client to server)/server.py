import socket
import threading


def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if message.lower() == 'terminate':
            print("Client disconnected.")
            client_socket.close()
            break
        print(f"Received: {message}")


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server started, listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
