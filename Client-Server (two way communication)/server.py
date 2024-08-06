import socket
import threading

clients = []


def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            if message.lower() == 'terminate':
                print(f"Client {addr} requested disconnection.")
                client_socket.close()
                clients.remove(client_socket)
                break
            print(f"Received from {addr}: {message}")
            broadcast_message(message, client_socket)
        except ConnectionResetError:
            print(f"Client {addr} forcibly closed the connection.")
            client_socket.close()
            clients.remove(client_socket)
            break


def broadcast_message(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message.encode())


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server started, listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
