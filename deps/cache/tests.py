# coding=utf-8
import random
import time
import threading
import unittest
from lru_cache import LruCache


class TesLruCache(unittest.TestCase):
    def test_cache_normal(self):
        a = []

        @LruCache(maxsize=2, timeout=1)
        def bar(num):
            a.append(num)
            return num

        bar(1)
        bar(1)
        self.assertEqual(a, [1])

    def test_cache_none(self):
        a = []

        @LruCache(maxsize=2, timeout=1)
        def bar(num):
            a.append(num)
            return None

        bar(1)
        bar(1)
        self.assertEqual(a, [1])

    def test_cache_when_timeout(self):
        a = []

        @LruCache(maxsize=2, timeout=1)
        def bar(num):
            a.append(num)
            return num

        bar(2)
        time.sleep(2)
        bar(2)
        self.assertEqual(a, [2, 2])

    def test_cache_when_cache_is_full(self):
        a = []

        @LruCache(maxsize=2, timeout=1)
        def bar(num):
            a.append(num)
            return num

        bar(1)
        bar(2)
        bar(3)
        bar(1)
        self.assertEqual(a, [1, 2, 3, 1])

    def test_cache_with_multi_thread(self):
        a = []

        @LruCache(maxsize=10, timeout=1)
        def bar(num):
            a.append(num)
            return num

        for i in xrange(10):
            threading.Thread(target=bar, args=(i, )).start()

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

        bar(random.randint(0, 9))
        self.assertEqual(set(a), set(range(10)))

    def test_cache_with_multi_thread_two_func(self):
        a = []

        @LruCache(maxsize=10, timeout=1)
        def bar(num):
            a.append(num)
            return num

        b = []

        @LruCache(maxsize=10, timeout=1)
        def bar(num):
            b.append(num)
            return num + 1

        for i in xrange(10):
            threading.Thread(target=bar, args=(i, )).start()
            threading.Thread(target=bar, args=(i, )).start()

        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()

        feed = random.randint(0, 9)
        self.assertEqual(bar(feed), feed)
        self.assertEqual(bar(feed), feed + 1)
        self.assertEqual(set(a), set(range(10)))
        self.assertEqual(set(b), set(range(10)))

    def test_cache_when_timeout_and_maxsize_is_none(self):
        a = []

        @LruCache()
        def bar(num):
            a.append(num)
            return num

        bar(1)
        bar(1)
        self.assertEqual(a, [1])

    def test_cache_when_timeout_is_none(self):
        a = []

        @LruCache(maxsize=10)
        def bar(num):
            a.append(num)
            return num

        bar(1)
        bar(1)
        self.assertEqual(a, [1])

    def test_cache_when_only_maxsize_is_none_normal(self):
        a = []

        @LruCache(timeout=2)
        def bar(num):
            a.append(num)
            return num

        bar(1)
        bar(1)
        self.assertEqual(a, [1])

    def test_cache_when_only_maxsize_is_none_timeout(self):
        a = []

        @LruCache(timeout=1)
        def bar(num):
            a.append(num)
            return num

        bar(1)
        time.sleep(2)
        bar(1)
        self.assertEqual(a, [1, 1])

    def test_cache_when_only_maxsize_is_none_normal_method(self):
        a = []

        class Func(object):
            @LruCache(timeout=2)
            def bar(self, num):
                a.append(num)
                return num

        fun = Func()
        fun.bar(1)
        fun.bar(1)
        self.assertEqual(a, [1])

    def test_cache_when_only_maxsize_is_none_normal_method_timeout(self):
        a = []

        class Func(object):
            @LruCache(timeout=1)
            def bar(self, num):
                a.append(num)
                return num

        fun = Func()
        fun.bar(1)
        time.sleep(2)
        fun.bar(1)
        self.assertEqual(a, [1, 1])

    def test_invalidate(self):
        a = []

        @LruCache()
        def bar(num):
            a.append(num)
            return num

        bar(1)
        bar(1)
        self.assertEqual(a, [1])
        bar.invalidate(1)
        bar(1)
        self.assertEqual(a, [1, 1])


if __name__ == "__main__":
    unittest.main()
