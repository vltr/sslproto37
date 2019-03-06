import os
import ssl

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


@pytest.fixture
def server_ctx():
    return server_ssl_context()


@pytest.fixture
def client_ctx():
    return client_ssl_context()
