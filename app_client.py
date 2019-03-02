import datetime
import socket
import time
from threading import Thread


def create_client_sockets():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect(("127.0.0.1", 12345))
    print("Client send socket connected")
    rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rec_socket.connect(("127.0.0.1", 12345))
    print("Client receive socket connected")
    return send_socket, rec_socket


def send_to_server_thread(send_socket):
    while True:
        current_dt = datetime.datetime.now()
        data = str(current_dt)
        data = data.encode("utf8")
        send_socket.sendall(data)
        time.sleep(1)


def get_from_server_thread(rec_socket):
    while True:
        data = rec_socket.recv(4096)
        data = data.decode("utf8")
        print("Received " + data)


def client_input_thread(send_to_server):
    print("Send commands as the client")
    while True:
        data = input(">")
        data = data.encode("utf8")
        send_to_server.sendall(data)


def main():
    send_socket, rec_socket = create_client_sockets()
    Thread(target=send_to_server_thread, args=(send_socket,)).start()
    Thread(target=get_from_server_thread, args=(rec_socket,)).start()


main()
