import psutil
import threading
from multiThreading.task import Task, AsyncTask
from multiThreading.queue import ThreadSafeQueue
from multiThreading.error import TaskTypeErrorException


class ProcessThread(threading.Thread):

    def __init__(self, task_queue, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        # 线程停止的标记
        self.dismiss_flag = threading.Event()
        # 任务队列（处理线程不断的从队列中取出元素处理）
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while True:
            # 判断线程是否要求停止
            if self.dismiss_flag.is_set():
                break
            task = self.task_queue.pop()
            if not isinstance(task, Task):
                continue
            # 执行task实际逻辑
            result = task.callable(*task.args, **task.kwargs)
            if isinstance(task, AsyncTask):
                task.set_result(result)

    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()


class ThreadPool:

    def __init__(self, size=0):
        if not size:
            # 约定线程池的大小为CPU核数的两倍
            size = psutil.cpu_count() * 2
        # 线程池
        self.pool = ThreadSafeQueue(size)
        # 任务队列
        self.task_queue = ThreadSafeQueue()

        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    # 启动线程池
    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    # 停止线程池
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()

    # 往线程池提交任务
    def put(self, item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException()
        self.task_queue.put(item)

    # 批量提交
    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.pool.put(item)

    def size(self):
        return self.pool.size()

