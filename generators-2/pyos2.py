from queue import Queue

from pyos1 import Task

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
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

            import time
            time.sleep(0.1)

if __name__ == '__main__':
    def foo():
        for i in range(10):
            print("Im foo")
            yield

    def bar():
        for i in range(20):
            print("Im bar")
            yield

    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()
