import threading
import socket

host = "localhost"
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []

def broadcast(message):
    message += "\n".encode('utf-8') #hesa
    for client in clients:
        try:
            if not isinstance(message, bytes):
                message = message.encode('utf-8')
            client.send(message)
        except Exception as e:
            print(f"Error broadcasting message: {e}")

 
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            message += "\n".encode('utf-8') 
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room.'.encode('utf-8'))
            aliases.remove(alias)
            break


def recieve():
    while True:
        print('Server is runing and listening...')
        client, address = server.accept()
        print(f'Connection is estabilshed with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        clients.append(client)
        aliases.append(alias)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('You are connected!'.encode('utf-8'))
        thread = threading.Thread(target= handle_client, args=(client,))
        thread.start()

recieve()

for thread in threading.enumerate():
    if thread != threading.current_thread():
        thread.join()
