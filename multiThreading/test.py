import time
from multiThreading import task, pool


class SimpleTask(task.Task):
    def __init__(self, callable):
        super(SimpleTask, self).__init__(callable)


def process():
    time.sleep(1)
    print("This is a simple callable function 11111.\n")
    time.sleep(1)
    print("This is a simple callable function 22222.\n")


def test():
    # 初始化一个线程池
    test_pool = pool.ThreadPool(2)
    test_pool.start()
    # exit()
    # 生成一系列任务
    for i in range(10):
        simple_task = SimpleTask(process)
        test_pool.put(simple_task)
    # 往线程池提交任务执行


def test_async():
    # 初始化一个线程池
    test_pool = pool.ThreadPool(2)
    test_pool.start()

    def async_func():
        num = 0
        for i in range(150):
            num += i
        time.sleep(1)
        return num
    # 生成一系列任务
    for i in range(10):
        simple_async_task = task.AsyncTask(async_func)
        print("the time of putting in: ", time.time())
        test_pool.put(simple_async_task)
        result = simple_async_task.get_result()
        print("the time of getting out: ", time.time())
        print(result)
    # 往线程池提交任务执行


def test_async_no_wait():
    # 初始化一个线程池
    test_pool = pool.ThreadPool(2)
    test_pool.start()

    def async_func():
        num = 0
        for i in range(150):
            num += i
        # time.sleep(1)
        return num
    # 生成一系列任务
    for i in range(10):
        simple_async_task = task.AsyncTask(async_func)
        print("the time of putting in: ", time.time())
        test_pool.put(simple_async_task)
        time.sleep(5)
        result = simple_async_task.get_result()
        print("the time of getting out: ", time.time())
        print(result)
    # 往线程池提交任务执行


if __name__ == '__main__':
    # test()
    # test_async()
    test_async_no_wait()
