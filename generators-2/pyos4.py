from queue import Queue

from pyos1 import Task

class SystemCall:
    def handle(self):
        pass

class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


class Scheduler:
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}

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

    def mainloop(self):
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
        for i in range(10):
            print(f"Im foo {mytid}")
            yield

    def bar():
        mytid = yield GetTid()
        for i in range(20):
            print(f"Im bar {mytid}")
            yield

    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()
