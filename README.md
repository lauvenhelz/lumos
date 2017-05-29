# lumos

server.py and socket_client.py for tests purposes only

To launch lantern client (host and port arguments can be omitted,
default values are host=127.0.0.1, port=9999):

    python3 tornado_client.py -H 127.0.0.2 -p 8888

Lantern module (lumos) also can be used from command line:

    echo -n 12 00 00 13 00 00 20 00 03 ff ff ff | xxd -r -p | python3 lumos.py
