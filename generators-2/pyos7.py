import select
from queue import Queue

from pyos1 import Task
from pyos4 import SystemCall, GetTid
from pyos5 import NewTask


class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforread(self.task, fd)


class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforwrite(self.task, fd)


class Scheduler:
    def __init__(self):
        self.ready = Queue()
        self.exit_waiting = {}
        self.taskmap = {}
        self.read_waiting = {}
        self.write_waiting = {}

    def waitforread(self, task, fd):
        self.read_waiting[fd] = task

    def waitforwrite(self, task, fd):
        self.write_waiting[fd] = task

    def iopool(self, timeout):
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting, self.write_waiting,
                                    [], timeout)
            for fd in r:
                self.schedule(self.read_waiting.pop(fd))

            for fd in w:
                self.schedule(self.write_waiting.pop(fd))

    def iotask(self):
        while True:
            if self.ready.empty():
                self.iopool(None)
            else:
                self.iopool(0)
            yield

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.put(task)

    def exit(self, task):
        print(f'Task {task.tid} terminated')
        del self.taskmap[task.tid]
        # Notify other tasks waiting for exit
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)

    def waitingforexit(self, task, waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid, []).append(task)
            return True
        else:
            return False

    def mainloop(self):
        self.new(self.iotask())

        while self.taskmap:
            task = self.ready.get()

            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

            import time
            time.sleep(0.1)


if __name__ == '__main__':
    def foo():
        mytid = yield GetTid()
        for i in range(5):
            print(f"Im foo {mytid}")
            yield

            import time
            time.sleep(0.1)

    def main():
        child = yield NewTask(foo())
        print('waiting for child')
        yield WaitTask(child)

        print('child done')
        print('main done')

    sched = Scheduler()
    sched.new(main())
    sched.mainloop()
