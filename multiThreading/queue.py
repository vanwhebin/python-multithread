
import time
import threading
import random

from multiThreading.error import ThreadSafeQueueException


class ThreadSafeQueue(object):
    """
    创建一个线程安全的队列类
    """
    def __init__(self, max_size=0):
        self.queue = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.condition = threading.Condition()

    # 获取队列的长度
    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    # 向队列中放入元素
    def put(self, item):
        if self.max_size != 0 and self.size() > self.max_size:
            return ThreadSafeQueueException()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        # 假设队列为0，线程阻塞，则队列能通知线程进行处理
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    # 批量放入元素
    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)

    # 从队列中取出元素，默认是头部元素
    def pop(self, block=False, timeout=None):
        if self.size() == 0:
            # 如果需要阻塞等待, 则需要通知线程
            if block:
                self.condition.acquire()
                self.condition.wait(timeout=timeout)
                self.condition.release()
            else:
                return None
        self.lock.acquire()
        item = None
        if len(self.queue) > 0:
            item = self.queue.pop()
        self.lock.release()
        return item

    # 获取队列中的元素
    def get(self, index):
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item


if __name__ == '__main__':
    queue = ThreadSafeQueue(max_size=100)

    def producer():
        while True:
            i = random.randint(1, 999)
            queue.put(i)
            print("put ", i, "into the queue")
            time.sleep(2)

    def consumer():
        while True:
            item = queue.pop(block=True, timeout=2)
            print("get item from queue: ", item)
            time.sleep(1)

    thread1 = threading.Thread(target=producer)
    thread2 = threading.Thread(target=consumer)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()





