import asyncio
import os
import sys

from contextlib import contextmanager
from unittest import mock

import pytest


IS_PY37 = sys.version_info[:2] > (3, 6)
skip_if_py37 = pytest.mark.skipif(
    IS_PY37,
    reason="should only be used with Python 3.5 and 3.6"
)


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        assert data == b"HELLO"
        self.transport.write(data)
        self.transport.close()


class EchoClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        transport.write(b"HELLO")


def ssl_protocol(loop, sslcontext, waiter=None, proto=None):
    """Function backported from Python 3.7.2"""
    from sslproto37 import SSLProtocolBackport

    if proto is None:  # app protocol
        proto = asyncio.Protocol()
    ssl_proto = SSLProtocolBackport(loop, proto, sslcontext, waiter,
                                    ssl_handshake_timeout=0.1)
    assert ssl_proto._app_transport.get_protocol() is proto
    return ssl_proto


def run_briefly(loop):
    """Function backported from Python 3.7.2"""
    async def once():
        pass
    gen = once()
    t = loop.create_task(gen)
    # Don't log a warning if the task is not done after run_until_complete().
    # It occurs if the loop is stopped or if a task raises a BaseException.
    t._log_destroy_pending = False
    try:
        loop.run_until_complete(t)
    finally:
        gen.close()


def connection_made(ssl_proto, *, do_handshake=None):
    """Function backported from Python 3.7.2"""
    transport = mock.Mock()
    sslpipe = mock.Mock()
    sslpipe.shutdown.return_value = b''
    if do_handshake:
        sslpipe.do_handshake.side_effect = do_handshake
    else:
        def mock_handshake(callback):
            return []
        sslpipe.do_handshake.side_effect = mock_handshake
    with mock.patch('asyncio.sslproto._SSLPipe', return_value=sslpipe):
        ssl_proto.connection_made(transport)
    return transport


@contextmanager
def env_variables(**kwargs):
    clashing_kwargs = {}
    for k, v in kwargs.items():
        if k in os.environ:
            clashing_kwargs[k] = os.environ[k]
        os.environ[k] = v
    yield
    for k, v in kwargs.items():
        os.environ.pop(k)
    for k, v in clashing_kwargs.items():
        os.environ[k] = v


@pytest.mark.skipif(not IS_PY37, reason="test made only for Python 3.7")
def test_warning_on_py37(recwarn):
    from sslproto37 import SSLProtocolBackportLoopPolicy
    assert len(recwarn) == 1
    assert recwarn.pop(ImportWarning)


@skip_if_py37()
def test_handshake_timeout_zero(client_ctx):
    from sslproto37 import SSLProtocolBackport

    loop = asyncio.get_event_loop()
    app_proto = mock.Mock()
    waiter = mock.Mock()
    with pytest.raises(ValueError):
        SSLProtocolBackport(loop, app_proto, client_ctx, waiter,
                            ssl_handshake_timeout=0)


@skip_if_py37()
def test_handshake_timeout_negative(client_ctx):
    from sslproto37 import SSLProtocolBackport

    loop = asyncio.get_event_loop()
    app_proto = mock.Mock()
    waiter = mock.Mock()
    with pytest.raises(ValueError):
        SSLProtocolBackport(loop, app_proto, client_ctx, waiter,
                            ssl_handshake_timeout=-10)


@skip_if_py37()
def test_successful_echo_default_timeout(server_ctx, client_ctx, free_port):
    from sslproto37 import SSLProtocolBackportLoopPolicy

    asyncio.set_event_loop_policy(SSLProtocolBackportLoopPolicy())
    loop = asyncio.get_event_loop()
    port = free_port()

    server = loop.create_server(
        EchoServerProtocol,
        "127.0.0.1",
        port,
        ssl=server_ctx
    )

    async def client():
        await loop.create_connection(
            EchoClientProtocol,
            '127.0.0.1',
            port,
            ssl=client_ctx
        )

    asyncio.ensure_future(server, loop=loop)
    loop.run_until_complete(asyncio.wait_for(client(), loop=loop, timeout=10))


@skip_if_py37()
def test_successful_echo_custom_timeout(server_ctx, client_ctx, free_port):

    with env_variables(PYSSLPROTO37_HANDSHAKE_TIMEOUT="30"):
        from sslproto37 import SSLProtocolBackportLoopPolicy

        asyncio.set_event_loop_policy(SSLProtocolBackportLoopPolicy())
        loop = asyncio.get_event_loop()
        port = free_port()

        server = loop.create_server(
            EchoServerProtocol,
            "127.0.0.1",
            port,
            ssl=server_ctx
        )

        async def client():
            await loop.create_connection(
                EchoClientProtocol,
                '127.0.0.1',
                port,
                ssl=client_ctx
            )

        asyncio.ensure_future(server, loop=loop)
        loop.run_until_complete(
            asyncio.wait_for(client(), loop=loop, timeout=10)
        )


@skip_if_py37()
def test_close_during_handshake(server_ctx):
    """Test backported from Python 3.7.2"""
    from sslproto37 import SSLProtocolBackportLoopPolicy

    asyncio.set_event_loop_policy(SSLProtocolBackportLoopPolicy())
    loop = asyncio.get_event_loop()

    # bpo-29743 Closing transport during handshake process leaks socket
    waiter = asyncio.Future(loop=loop)
    ssl_proto = ssl_protocol(loop, server_ctx, waiter=waiter)

    transport = connection_made(ssl_proto)
    run_briefly(loop)

    ssl_proto._app_transport.close()
    assert transport.abort.called


@skip_if_py37()
def test_eof_received_waiter(server_ctx):
    """Test backported from Python 3.7.2"""
    from sslproto37 import SSLProtocolBackportLoopPolicy

    asyncio.set_event_loop_policy(SSLProtocolBackportLoopPolicy())
    loop = asyncio.get_event_loop()

    waiter = asyncio.Future(loop=loop)
    ssl_proto = ssl_protocol(loop, server_ctx, waiter=waiter)
    connection_made(ssl_proto)
    ssl_proto.eof_received()
    run_briefly(loop)
    assert isinstance(waiter.exception(), ConnectionResetError)


@skip_if_py37()
def test_ssl_handshake_timeout(server_ctx, free_port):

    with env_variables(PYSSLPROTO37_HANDSHAKE_TIMEOUT="3"):
        from sslproto37 import SSLProtocolBackportLoopPolicy

        asyncio.set_event_loop_policy(SSLProtocolBackportLoopPolicy())
        loop = asyncio.get_event_loop()
        port = free_port()

        server = loop.create_server(
            EchoServerProtocol,
            "127.0.0.1",
            port,
            ssl=server_ctx
        )

        async def client():
            reader, writer = await asyncio.open_connection(
                "127.0.0.1", port, loop=loop
            )
            await asyncio.sleep(5)

        asyncio.ensure_future(server, loop=loop)
        loop.run_until_complete(
            asyncio.wait_for(client(), loop=loop, timeout=60)
        )
