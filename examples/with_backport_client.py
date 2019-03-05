import asyncio
import os
import ssl
import sys

sys.path.append(os.path.join(".."))

from sslproto37 import SSLProtocolBackportLoopPolicy

root_path = os.path.dirname(os.path.abspath(__file__))
ssl_cert = os.path.join(root_path, "server.crt")


def dumb_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.check_hostname = False
    ctx.load_verify_locations(ssl_cert)
    return ctx


class EchoClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        message = b"HELLO"
        transport.write(message)
        print('Data sent: {!r}'.format(message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')


def main():
    asyncio.set_event_loop_policy(SSLProtocolBackportLoopPolicy())
    loop = asyncio.get_event_loop()

    async def client():
        await loop.create_connection(
            EchoClientProtocol,
            '127.0.0.1',
            8888,
            ssl=dumb_ssl_context(),
            server_hostname=''
        )

    loop.run_until_complete(asyncio.wait_for(client(), loop=loop, timeout=10))


if __name__ == "__main__":
    main()
