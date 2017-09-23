from functools import wraps

from concurrent.futures import ThreadPoolExecutor
from gevent.pool import Pool as GPool


class Tomorrow:
    def __init__(self, future, timeout):
        self._future = future
        self._timeout = timeout

    @property
    def res(self):
        return self._wait()

    def _wait(self):
        return self._future.result(self._timeout)


class GTomorrow:
    def __init__(self, future, timeout):
        self._future = future
        self._timeout = timeout

    @property
    def res(self):
        return self._wait()

    def _wait(self):
        self._future.join()
        return self._future.value


def multiprocess_patch(n, base_type, timeout=None):
    def decorator(f):
        if isinstance(n, int):
            pool = base_type(n)
        elif isinstance(n, base_type):
            pool = n
        else:
            raise TypeError(
                "Invalid type: %s"
                % type(base_type)
            )

        @wraps(f)
        def wrapped(*args, **kwargs):
            return Tomorrow(
                pool.submit(f, *args, **kwargs),
                timeout=timeout
            )

        return wrapped

    return decorator


def gevent_patch(n, timeout=None):
    from gevent import monkey
    monkey.patch_all()

    def decorator(f):
        pool = GPool(n)

        @wraps(f)
        def wrapped(*args, **kwargs):
            return GTomorrow(
                pool.spawn(f, *args, **kwargs), timeout
            )

        return wrapped

    return decorator


def threads(n, run_mode=None, timeout=None):
    if run_mode is None or run_mode == 'sync':
        return multiprocess_patch(n, ThreadPoolExecutor, timeout)
    elif run_mode == 'async':
        return gevent_patch(n, timeout)
    else:
        raise Exception('No run mode installed for {}'.format(run_mode))


