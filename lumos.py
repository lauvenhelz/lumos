import sys
import struct

hs = struct.Struct('!BH')


class Parser(object):
    def __init__(self):
        self.tail = None

    def parse(self, buffer):
        if self.tail:
            buffer = self.tail + buffer

        while buffer:
            header = buffer[:hs.size]

            if not len(header) == hs.size:
                self.tail = buffer
                break

            command_type, length = hs.unpack(header)
            value = buffer[hs.size:hs.size + length]

            if len(value) < length:
                self.tail = buffer
                break

            buffer = buffer[hs.size + length:]

            yield command_type, value

    def reset(self):
        self.tail = None


def execute_command(command, value):
    commands.get(command, invalid_command)(value)


def on(value):
    print('Lantern is on')


def off(value):
    print('Lantern is off')


def change_color(value):
    color = struct.unpack('!BBB', value[:3])
    print('Lantern changed color to: {}'.format(color))


def invalid_command(value):
    pass


commands = {0x12: on,
            0x13: off,
            0x20: change_color}

if __name__ == '__main__':
    # example:
    # echo -n 12 00 00 13 00 00 20 00 03 ff ff ff | xxd -r -p | python lumos.py
    p = Parser()
    for cmd, vl in p.parse(sys.stdin.buffer.read(8000)):
        execute_command(cmd, vl)
