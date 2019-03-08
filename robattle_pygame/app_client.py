import json
import queue
import socket
from threading import Thread

from robattle_pygame.main_game import launch_game

endgame = False

server_queue = queue.Queue()


def create_client_sockets():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect(("127.0.0.1", 12345))
    print("Client send socket connected")
    rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rec_socket.connect(("127.0.0.1", 12345))
    print("Client receive socket connected")
    return send_socket, rec_socket


def get_from_server_thread(rec_socket):
    global endgame
    while not endgame:
        data = rec_socket.recv(4096)
        if data == b'':
            print("Terminating Client")
            endgame = True
            break
        data = data.decode("utf8")
        print("Received " + data)


def send_to_server(send_socket):
    global endgame
    print("Send commands as the client")
    while not endgame:
        data = server_queue.get()
        data = json.dumps(data)
        data = data.encode("utf8")
        send_socket.sendall(data)


def main():
    send_socket, rec_socket = create_client_sockets()
    Thread(target=send_to_server, args=(send_socket,)).start()
    # Thread(target=send_to_server_thread, args=(send_socket,)).start()
    Thread(target=get_from_server_thread, args=(rec_socket,)).start()
    launch_game(server_queue)


main()
