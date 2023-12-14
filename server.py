import socket
import threading
import hashlib
users = {}
clients = {}
socketUsers = {} #this dict takes in a socket and gives the user accordingly
usersSockets = {}#this dict takes in a username and gives the socket accordingly.
busy_clients = set()
chatGroupUsers = {}#this dict takes in a group name and it's member's usernames.

def request_handler(request, username, client_socket):
    requestSp = request.split(':')
    if requestSp[0] == 'disconnect':
        print('disconnection request')
        clients[client_socket] = None
        client_socket.close()
        exit(0)
    elif requestSp[0] == 'broadcast' and len(requestSp) > 1:
        text = f"{username} broadcasts: {requestSp[1]} "
        for c in clients:
            if c is not None:
                c.send(text.encode('utf-8'))
    elif requestSp[0] == 'send' and len(requestSp) > 2:
        text = requestSp[1]
        receiver = requestSp[2]
        for u in usersSockets:
            if u == receiver:
                currSocket = usersSockets[u]
                if currSocket is not None:
                    u.send(text.encode('utf-8'))
                    break
    elif requestSp[0] == 'sendgp' and len(requestSp) > 2:
        text = requestSp[1]
        gpReceiver = requestSp[2]
        for groupName in chatGroupUsers:
            if groupName == gpReceiver:
                for memberUsername in chatGroupUsers[groupName]:
                    memberSocket =





def handle_client(client_socket, client_address):
    authData = client_socket.recv(1024).decode('utf-8')
    authDataSp = authData.split(":")
    username, password = authDataSp[1], authDataSp[2]



    print(f"new user: {username}, {hash(password)}")
    client_socket.send("AUTH".encode('utf-8'))
    users[username] = hash(password)
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        request_handler(request, username, client_socket)



def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0',1235))
    server.listen(5)
    print("Server listening on port 1235")
    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()


if __name__ == "__main__":
    start_server()
