from pyos4 import SystemCall, Scheduler, GetTid

class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)


class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)


if __name__ == '__main__':
    def foo():
        mytid = yield GetTid()
        while True:
            print(f"Im foo {mytid}")
            yield

            import time
            time.sleep(0.1)

    def main():
        child = yield NewTask(foo())
        for i in range(5):
            yield

        yield KillTask(child)
        print('main done')

    sched = Scheduler()
    sched.new(main())
    sched.mainloop()
