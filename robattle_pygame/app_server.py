import pickle
import queue
import socket
import sys
from threading import Thread

clients = []
MAX_CLIENTS = 2
messages = queue.Queue()


def create_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')
    try:
        server.bind(("127.0.0.1", 12345))
        print('Socket binded')
    except socket.error as error:
        print(error)
        sys.exit()
    server.listen(4)
    print("Socket listening...")
    return server


def send_to_all_clients():
    while True:
        player, data = messages.get()
        for client in clients:
            player_ip_port = str(player['ip']) + str(player['port'])
            client_ip_port = str(client[2]) + str(client[3])
            if client_ip_port != player_ip_port:
                client[1].sendall(data)


"""Make dictionary for each client, every time client sends message add to that queue,
 then in another method read values from queue and send to all clients"""


def client_thread(rec_socket, ip, port, max_buffer_size=4096):
    while True:
        data = rec_socket.recv(max_buffer_size)
        if data == b'':
            rec_socket.close()
            print("Player from " + ip + ":" + port + " has left")
            break
        player = pickle.loads(data)
        print("Player sent", player)
        messages.put((player, data))


def run_server(server):
    while len(clients) < MAX_CLIENTS:
        rec_socket, rec_addr = server.accept()
        send_socket, send_addr = server.accept()
        ip, port = str(rec_addr[0]), str(rec_addr[1])
        print("Player from " + ip + ":" + port + " has joined")
        clients.append((rec_socket, send_socket, ip, port))
        Thread(target=client_thread, args=(rec_socket, ip, port)).start()
    print("All Players Have Joined")
    print("Get Ready to Robattle!!!")
    # Add reset message to queue python now that game begins
    # messages.put("reset")

    # server.close()


def main():
    server = create_server_socket()
    run_server(server)
    send_to_all_clients()


main()
