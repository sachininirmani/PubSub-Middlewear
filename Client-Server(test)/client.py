import socket


def start_client(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print(f"[Connected to the Server at {ip}  -  port {port}]")

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

    if len(sys.argv) != 3:
        print("Usage: python client.py  <SERVER_IP> <SERVER_PORT> ")
        sys.exit(1)

    server_ip = (sys.argv[1])
    server_port = int(sys.argv[2])
    start_client(server_ip, server_port)
