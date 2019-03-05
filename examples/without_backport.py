import asyncio
import os
import ssl

root_path = os.path.dirname(os.path.abspath(__file__))
ssl_cert = os.path.join(root_path, "server.crt")
ssl_key = os.path.join(root_path, "server.key")


def dumb_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.check_hostname = False
    ctx.load_cert_chain(ssl_cert, ssl_key)
    return ctx


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


def main():
    loop = asyncio.get_event_loop()
    server = loop.create_server(
        EchoServerProtocol,
        "127.0.0.1",
        8888,
        ssl=dumb_ssl_context()
    )
    asyncio.ensure_future(server, loop=loop)
    loop.run_forever()


if __name__ == "__main__":
    main()
