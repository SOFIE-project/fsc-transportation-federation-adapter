import asyncio
from functools import wraps

from syncer import sync


def try_sync(f):
    """ Asyncio event loop support for when running async code in django-middleware.

    Solves problems like this:
        RuntimeError: There is no current event loop in thread 'DummyThread-1'
    """
    @wraps(f)
    def run(*args, **kwargs):
        try:
            return sync(f(*args, **kwargs))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = loop.run_until_complete(f(*args, **kwargs))
            loop.close()
            return res
    return run
