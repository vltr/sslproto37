# sslproto37

[![Build Status](https://travis-ci.org/vltr/sslproto37.svg?branch=master)](https://travis-ci.org/vltr/sslproto37)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/vltr/sslproto37?branch=master&svg=true)](https://ci.appveyor.com/project/vltr/sslproto37)
[![Coverage Status](https://codecov.io/github/vltr/sslproto37/coverage.svg?branch=master)](https://codecov.io/github/vltr/sslproto37)

**ATTENTION:** this is not a PyPI package and it is not intended to be used as one (IMHO).

This is a simple backport of the `SSLProtocol` from Python 3.7 that adds a SSL handshake timeout feature, that does not exists in Python 3.5 and Python 3.6.

## Who needs this backport

Everyone that uses a SSL context to their `asyncio` servers under Python 3.5 or Python 3.6 with the default `asyncio` loop policy.

## Who doesn't needs this backport

Anyone using Python 3.7 or an alternative `asyncio` event loop such as `uvloop`, which already implements a default SSL handshake timeout and works under Python 3.5 and 3.6.

## The importance of this backport

Without the SSL handshake timeout, one can simple open a connection to your server (using telnet) and _never_ perform a SSL handshake, exhausting your server available connections and leaving it non-responsive, which can lead to a DOS attack.

## Using `sslproto37`

All you need to do is copy the source code to your own project and make it work there, such as:

```python
import asyncio
import sys

if sys.version_info < (3, 7):  # test if you really need this backport
    from .sslproto37 import SSLProtocolBackportLoopPolicy

    asyncio.set_event_loop_policy(SSLProtocolBackportLoopPolicy())

```

In case you copy the test case as well, make sure it is not ran if the Python version is 3.7 (or above).

### Configuring the SSL handshake timeout parameter

Since this is only a very simple backport, not all function calls and parameters came to light to avoid a complex code. So, the SSL handshake timeout time is set to `60` seconds as default inside the code, but it can be changed if you set the `PYSSLPROTO37_HANDSHAKE_TIMEOUT` system variable to another value that _should be converted_ to `float` **and** above `0.0`. The actual value you set is completely your choice and should take into consideration deployment best practices that I would not discuss in here.

### Testing

You can check the test coverage of this protocol with the badge right at the beggining of this README. It is tested against Python 3.5, 3.6 _and_ 3.7 (where a nice `warning` should be in place in case you forgot this is not intended to use with Python 3.7) and all tests can be run by `tox`. **Note**: some warnings and nested exceptions might occur while testing under Python 3.5. PRs are welcome to solve that issue but the goal was to make this work.

## Many thanks to

- [Phil Jones - @pgjones](https://github.com/pgjones)
- [Tom Christie - @tomchristie](https://github.com/tomchristie)

For bringing us (the [Sanic](https://github.com/huge-success/sanic) team) the attention for this matter.
