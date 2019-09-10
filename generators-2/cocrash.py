from cothread import threaded, threaded_safe
from cobroadcast import broadcast
from copipe import grep
from cofollow import printer

p = printer()

target = broadcast([
    threaded(grep('foo', p)),
    threaded(grep('bar', p)),
])

# target = broadcast([
#     threaded_safe(grep('foo', p)),
#     threaded_safe(grep('bar', p)),
# ])

for i in range(100):
    target.send('foo is nice - %d' % i)
    target.send('bar is bad - %d' % i)

del p
del target
