import socket
import threading

SERVER_IP = socket.gethostbyname(socket.gethostname())
print(SERVER_IP)

clients = []


def handle_client(client, addr, server):
    connected = True
    while connected:
        message_from_client = client.recv(1024).decode()
        if message_from_client.lower() == "terminate":
            terminated = False
            print(f"[Client: {addr} requests disconnection from Server] (enter granted to terminate): ")
            while not terminated:
                grant_msg = input("")
                client.send(grant_msg.encode())

                if grant_msg == "granted":
                    print(f"[Client :  {addr} Disconnected from Server]")
                    clients.remove(client)
                    client.close()
                    print(f"[{len(clients)} Clients are Remaining]")
                    # if len(clients) == 0:
                    #     print(f"[Server Stopping ... {SERVER_IP}]")
                    #     server.close()
                    terminated = True
                    connected = False
                    break

        else:
            print(f"[From Client  :  {addr} :- {message_from_client}]")


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, port))

    server_socket.listen(5)
    print(f"[Server Starting ... {SERVER_IP}]")

    while True:
        client_socket, client_addr = server_socket.accept()
        clients.append(client_socket)
        print(f"[Client - {client_addr} is Listening]")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_addr, server_socket))
        client_handler.start()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    server_port = int(sys.argv[1])
    start_server(server_port)

