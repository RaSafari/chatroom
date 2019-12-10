import socket
import time
import select
import random

IP = ''
PORT = 8216

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(10)

socket_list = [server_socket]
clients = {}
database={}
k=0
while True:
    read_socket, write_socket, exception_socket = select.select(
        socket_list, [], socket_list)

    for s in read_socket:
        if s == server_socket:
            client_socket, address = server_socket.accept()

            if client_socket:
                client_socket.send(bytes("welcome!\n for every chat, Enter one of tree choices with these formate:\n"
                                         " 1:username (for username register)\n"
                                         " 2 (for see member list)\n"
                                         " 3:yor contact:your meesege (for start chat with this person)\n" , 'utf-8'))
                socket_list.append(client_socket)
                user = address[0]
                clients[client_socket] = user

        else:
            message = s.recv(1024)
            message1 = message.decode('utf-8')
            message2 = message1.split(':')
            if not message:
                socket_list.remove(s)
                del clients[s]
                continue

            if message2[1] == '1':
               database[s] = message2[2]
            elif message2[1] == '2':
                for client_socket in clients:
                    s.send(bytes("{} ----".format(database[client_socket]),'utf-8'))
            elif message2[1] == '3':
                 for client_socket in clients:
                     if message2[2] == database[client_socket]:
                        k = 1
                        client_socket.send(bytes("{} ->".format(message2[0]), 'utf-8'))
                        client_socket.send(bytes(message2[3],'utf-8'))

                 if k==0:
                    s.send(bytes("your contacts is not online",'utf-8'))

            else:
                s.send(bytes("please enter correct format",'utf-8'))

    for s in exception_socket:
        socket_list.remove(s)
        del clients[s]
