import socket
from time import sleep
from itertools import cycle

data = [b'\x12\x00\x00', b'\x13\x00\x00', b'\x20\x00\x03\xff\xff\xff']

HOST = '127.0.0.2'
PORT = 9998

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        try:
            conn, address = s.accept()
            with conn:
                print('Connected by', address)
                for item in cycle(data):
                    conn.sendall(item)
                    sleep(1)
        except Exception as ex:
            print(ex)
