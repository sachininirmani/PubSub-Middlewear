import socket
import threading


def receive_messages(subscriber_socket):
    while True:
        message_directed_from_publishers = subscriber_socket.recv(1024).decode()
        print(f"\nDirected From server : {message_directed_from_publishers}")
        break


def start_client(ip, port, roll):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.send(roll.lower().encode())
    print(f"[Connected to the Server at {ip}  -  port {port} as a {roll.lower()}]")

    receive_publisher_messages = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_publisher_messages.start()

    connected = True
    while connected:

        message_from_client = input("Enter message : ")
        client_socket.send(message_from_client.encode())
        if message_from_client.lower() == "terminate":
            print(f"[Disconnection Requested from the Server]")
            granted = False
            while not granted:
                grant_disconnection = client_socket.recv(1024).decode()
                if grant_disconnection.lower() == "granted":
                    print(f"[Disconnection Granted. Client Terminated.]")
                    granted = True
                    break
                else:
                    print(f"From Server : {grant_disconnection}")
            connected = False
            break

    # client_socket.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python client.py  <SERVER_IP> <SERVER_PORT> <PUBLISHER | SUBSCRIBER>")
        sys.exit(1)

    server_ip = (sys.argv[1])
    server_port = int(sys.argv[2])
    client_roll = sys.argv[3]
    start_client(server_ip, server_port, client_roll)
