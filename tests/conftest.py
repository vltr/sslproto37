import os
import socket
import ssl

from contextlib import closing

import pytest

root_path = os.path.dirname(os.path.abspath(__file__))
ssl_cert = os.path.join(root_path, "..", "examples", "server.crt")
ssl_key = os.path.join(root_path, "..", "examples", "server.key")


def server_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.check_hostname = False
    ctx.load_cert_chain(ssl_cert, ssl_key)
    return ctx


def client_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.check_hostname = False
    ctx.load_verify_locations(ssl_cert)
    return ctx


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


@pytest.fixture
def server_ctx():
    return server_ssl_context()


@pytest.fixture
def client_ctx():
    return client_ssl_context()


@pytest.fixture
def free_port():
    return find_free_port
