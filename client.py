import socket
import threading

def authenticate(client_socket):
    username = input('please enter your username')
    password = input('please enter your password')
    msg = f"Auth:{username}:{password}"
    client_socket.send(msg.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "AUTH":
        return True
    else:
        return False

def send_message(client_socket):
    while True:
        recipient = input("Enter recipient's address (IP:PORT): ")
        message = input("Enter your message: ")
        data = f"{recipient}:{message}"
        client_socket.send(data.encode('utf-8'))

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received from server: {data.decode('utf-8')}")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 1235))

    if authenticate(client):
        print('hello!')
        send_thread = threading.Thread(target=send_message, args=(client,))
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        send_thread.start()
        receive_thread.start()

if __name__ == "__main__":
    start_client()
