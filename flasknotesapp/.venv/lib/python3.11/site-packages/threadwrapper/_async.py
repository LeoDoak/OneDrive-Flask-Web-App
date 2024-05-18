from omnitools import debug_info, p, randstr
import traceback
import asyncio
import time
import sys


class ThreadWrapper_async:
    def __init__(self, semaphore: asyncio.Semaphore, loop: asyncio.AbstractEventLoop) -> None:
        self.total_thread_count = 0
        self.sema = semaphore
        self.tasks = []
        self.loop = loop
        self.debug_time = False

    async def __run_job(self, job, result, key):
        response = None
        try:
            await self.sema.acquire()
            start_time = time.time()
            self.total_thread_count += 1
            response = await job
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
            self.sema.release()
            return response

    def add(self, *, job, result = None, key = None):
        if result is None:
            result = {}
            if key is None:
                key = randstr(128)
        else:
            if key is None:
                raise Exception("invalid key for result type {}".format(type(result).__name__))
        job = self.__run_job(job, result, key)
        job = asyncio.ensure_future(job, loop=self.loop)
        job.name = key
        self.tasks.append(job)
        return key

    async def cleanup(self):
        cancelled = []
        for task in self.tasks:
            try:
                if not task.done():
                    task.cancel()
                    cancelled.append(task)
            except:
                pass
        try:
            if not cancelled:
                return
            tasks, _ = await asyncio.wait(cancelled, loop=self.loop)
            for task in tasks:
                try:
                    await task.result()
                except:
                    pass
        except:
            pass
        finally:
            await self.loop.shutdown_asyncgens()

    def wait(self, run_type=None):
        async def main():
            return await asyncio.gather(*self.tasks, loop=self.loop)

        asyncio.set_event_loop(self.loop)
        result = None
        try:
            if run_type == "run_forever":
                self.loop.run_forever()
            else:
                self.loop.run_until_complete(main())
        except KeyboardInterrupt:
            pass
        except:
            result = traceback.format_exc()
        self.loop.run_until_complete(self.cleanup())
        return result

    def get_task_by_key(self, key: str) -> asyncio.Future:
        for task in self.tasks:
            if task.name == key:
                return task
        raise Exception("no task with key {}".format(key))

    def get_key_by_task(self, task: asyncio.Future) -> str:
        for _task in self.tasks:
            if _task == task:
                return _task.name
        raise Exception("no task {} found".format(str(task)))
