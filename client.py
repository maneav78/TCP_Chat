import threading
import socket

alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 59000))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'alias?':
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

def client_send():
    while True:
        message = input('Enter your message >>> \n')
        full_message = f'{alias}: {message}'
        client.send(full_message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
send_thread = threading.Thread(target=client_send)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()



 
