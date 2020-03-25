import threading
import time
from datetime import datetime
def term_thread(thread_id):
    # 强制结束线程
    import os
    if os.name == "nt":
        # windows 系统
        # 注意：线程结束后 threading.Thread 没有任何提示。
        import ctypes
        h = ctypes.windll.kernel32.OpenThread(1, 0, thread_id)
        assert h != 0
        r = ctypes.windll.kernel32.TerminateThread(h, 0xff)
        assert r != 0
    else:
        # TODO
        raise NotImplementedError


def run_thread():
    while 1:
        time.sleep(1)
        print('{}'.format(datetime.now()))


def main():
    t = threading.Thread(target=run_thread)
    t.start()

    time.sleep(3)
    # print(t.ident)
    term_thread(t.ident)

    # 强制结束线程导致 join() 永远不会返回
    # t.join()


if __name__ == '__main__':
    main()