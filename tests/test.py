import time
import unittest

from concurrent.futures import ThreadPoolExecutor, TimeoutError

from tomorrow import threads

DELAY = 0.5
TIMEOUT = 0.1
N = 2


class TomorrowTestCase(unittest.TestCase):

    def test_threads_decorator(self):
        def slow_add(x, y):
            time.sleep(DELAY)
            return x + y

        @threads(N)
        def async_add(x, y):
            time.sleep(DELAY)
            return x + y

        cur_x, cur_y = 2, 2

        start = time.time()

        results = []
        for i in range(N):
            results.append(async_add(cur_x, cur_y))

        checkpoint = time.time()

        for result in results:
            result._wait()

        end = time.time()
        assert (checkpoint - start) < DELAY
        assert DELAY < (end - start) < (DELAY * N)

    def test_shared_executor(self):

        executor = ThreadPoolExecutor(N)

        @threads(executor)
        def f(x):
            time.sleep(DELAY)
            return x

        @threads(executor)
        def g(x):
            time.sleep(DELAY)
            return x

        start = time.time()

        results = []
        for i in range(N):
            results.append(g(f(i)))

        for result in results:
            print(result._wait())

        end = time.time()
        assert (N * DELAY) < (end - start) < (2 * N * DELAY)


    def test_timeout(self):

        @threads(N, timeout=TIMEOUT)
        def raises_timeout_error():
            time.sleep(DELAY)
            return 1

        with self.assertRaises(TimeoutError):
            f = raises_timeout_error()
            print(dir(f))

        # @threads(N, timeout=2*DELAY)
        # def no_timeout_error():
        #     time.sleep(DELAY)
        #
        # print(no_timeout_error())

    def test_future_function(self):

        @threads(N)
        def returns_function():
            def f():
                return True
            return f

        true = returns_function()
        assert true()

    def test_wait(self):

        mutable = []

        @threads(N)
        def side_effects():
            mutable.append(True)

        result = side_effects()
        result._wait()
        assert mutable[0]

        @threads(N, timeout=0.1)
        def side_effects_timeout():
            time.sleep(1) 

        result = side_effects_timeout()
        with self.assertRaises(TimeoutError):
            result._wait()


if __name__ == "__main__":
    unittest.main()
