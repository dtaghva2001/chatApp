import socket
import threading
username = ""
password = ""
lock = threading.Lock()
def authenticate(client_socket):
    global username, password
    username = input('please enter your username   ')
    password = input('please enter your password    ')
    msg = f"Auth:{username}:{password}"
    client_socket.send(msg.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    if response == "AUTH":
        return True
    else:
        return False


def send_message(client_socket):
    while True:
        inp = int(input('enter your message type: 1) broadcast- 2) group 3) send 4)create group  '))
        with lock:
            print('start critical section')
            if inp == 'disconnect':
                mess = f"disconnect"

            if inp == 1:
                print('broadcasting started')
                broadcastTxt = input('please enter your text to broadcast: ')
                mess = f"broadcast:{broadcastTxt}"
                client_socket.send(mess.encode('utf-8'))
            elif inp == 2:
                print('group sending started')
            elif inp == 3:
                rec = input('please enter your receiver name: ')
                txt = input('please enter your text: ')
                mess = f"send:{txt}:{rec}"
                client_socket.send(mess.encode('utf-8'))
            elif inp == 4:
                groupName = input('please enter the group name ')
                groupIDs = [username]
                numberOfMembers = int(input('please enter number of group members  '))
                for i in range(numberOfMembers):
                    gId = input('please enter group member id ')
                    groupIDs.append(gId)
                mess = f'createGP:{groupName}:{groupIDs}'
                client_socket.send(mess.encode('utf-8'))
            print('end critical section')

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
