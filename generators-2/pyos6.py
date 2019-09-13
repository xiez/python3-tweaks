from queue import Queue

from pyos1 import Task
from pyos4 import SystemCall, GetTid
from pyos5 import NewTask, KillTask


class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.waitingforexit(self.task, self.tid)
        self.task.sendval = result
        if not result:
            self.sched.schedule(self.task)


class Scheduler:
    def __init__(self):
        self.ready = Queue()
        self.exit_waiting = {}
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
