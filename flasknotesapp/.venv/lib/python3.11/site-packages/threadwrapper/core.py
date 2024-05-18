from omnitools import p, debug_info, args, def_template, randstr
import threading
import time
import sys


class ThreadWrapper:
    def __init__(self, semaphore: threading.Semaphore) -> None:
        self.total_thread_count = 0
        self.threads = []
        self.sema = semaphore
        self.internal_lock = threading.Lock()
        self.debug_time = False
        self.alive_threads = []
        self.dead_threads = []
        self._alive_threads_ct = 0
        self._dead_threads_ct = 0

    @property
    def alive_threads_ct(self):
        with self.internal_lock:
            return self._alive_threads_ct

    @property
    def dead_threads_ct(self):
        with self.internal_lock:
            return self._dead_threads_ct

    def __run_job(self, job, result = None, key = None) -> None:
        response = None
        try:
            self.sema.acquire()
            start_time = time.time()
            self.total_thread_count += 1
            response = job()
            if isinstance(result, list):
                result.append(response)
            elif isinstance(result, dict):
                result[key] = response
            duration = time.time()-start_time
            if self.debug_time:
                count = str(self.total_thread_count).ljust(20)
                qualname = job.__qualname__.ljust(50)
                timestamp = str(int(time.time() * 1000) / 1000).ljust(20)[6:]
                s = "Thread {}{}{}{}s\n".format(count, qualname, timestamp, duration)
                if duration >= 0.5:
                    sys.stderr.write(s)
                    sys.stderr.flush()
                else:
                    p(s)
        except:
            response = debug_info()[0]
        finally:
            thread = self.get_thread_by_key(key)
            with self.internal_lock:
                self.alive_threads.remove(thread)
                self._alive_threads_ct -= 1
                # self.dead_threads.append(thread)
                self._dead_threads_ct += 1
            self.sema.release()
            return response

    def add(self, *, job, result = None, key = None) -> bool:
        if result is None:
            result = {}
            if key is None:
                key = randstr(128)
        else:
            if key is None:
                raise Exception("invalid key for result type {}".format(type(result).__name__))
        thread = threading.Thread(target=self.__run_job, args=(job, result, key))
        thread.name = key
        self.threads.append(thread)
        with self.internal_lock:
            self.alive_threads.append(thread)
            self._alive_threads_ct += 1
        thread.start()
        return key

    def wait(self) -> bool:
        n = 0
        while n < len(self.threads):
            self.threads[n].join()
            n += 1
        return True

    def get_thread_by_key(self, key: str) -> threading.Thread:
        for thread in self.threads:
            if thread.name == str(key):
                return thread
        raise Exception("no thread with key {}".format(key))

    def get_key_by_thread(self, thread: threading.Thread) -> str:
        for _thread in self.threads:
            if _thread == thread:
                return _thread.name
        raise Exception("no thread {} found".format(str(thread)))



