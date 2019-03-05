# Examples

There are some files in this example folder:

- `with_backport_client.py`: a simple client to run when either `with` or `without_backport.py` servers are running;
- `with_backport.py`: a simple echo server with the SSL handshake timeout implemented;
- `without_backport.py`: a simple echo server with default Python `asyncio` implementation.

**In case you're running Python 3.5 and 3.6**, if you call the above servers, you might notice that you can actually open a connection using `telnet` to your own echo servers, just like:

```
telnet 127.0.0.1 8888
```

And what will happens if running `telnet` against:

- `with_backport.py`: your connection will be closed after 60 seconds (unless you call the server with a different - and valid - `PYSSLPROTO37_HANDSHAKE_TIMEOUT` environment value);
- `without_backport.py`: your connection will be left open for a very, very, very, very, very long time. Very good for exhausting your server's available connections and leaving it non-responsive in a DOS attack scenario. This will not happen if you use `uvloop`, for example, since it implements SSL handshake timeout on its own.
