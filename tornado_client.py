import lumos
import signal
import socket
import argparse

from tornado import iostream, ioloop, gen

dead = False


async def main(host, port):
    global dead

    def exit_lantern(signum, frame):
        global dead
        dead = True
        print('\nLantern is over.')
        stream.close()

    signal.signal(signal.SIGINT, exit_lantern)
    signal.signal(signal.SIGTERM, exit_lantern)

    async def get_stream():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                strm = iostream.IOStream(s)
                await strm.connect((host, port))
                print('Lantern is here.')
                return strm
            except iostream.StreamClosedError:
                if not dead:
                    print('Trying to reconnect.')
                    await gen.sleep(1)
                else:
                    break

    stream = await get_stream()
    p = lumos.Parser()

    while stream:
        try:
            f = await stream.read_bytes(4096, partial=True)
        except iostream.StreamClosedError:
            if not dead:
                stream = await get_stream()
                p.reset()
            else:
                break
        else:
            for command, value in p.parse(f):
                lumos.execute_command(command, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, default=9999)
    args = parser.parse_args()

    io = ioloop.IOLoop.current()
    io.run_sync(lambda: main(args.host, args.port))
