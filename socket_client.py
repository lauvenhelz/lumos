import lumos
import socket

HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Lantern is here.')
    p = lumos.Parser()
    while True:
        for command, value in p.parse(s.recv(4096)):
            lumos.execute_command(command, value)
