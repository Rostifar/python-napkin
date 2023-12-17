## Python Concurrency

Building services in Python requires concurrency: multiple tasks being worked on at the same time but not in parallel.

The Global Interpreter Lock (GIL) ensures that no thread associated with a process runs in parallel. For CPU-intensive loads, this means exploiting multiprocessing in some fashion (e.g. using Celery to offload tasks from the main thread); note that Python actually has a thread called _MainThead! However, for IO-intensive operations — where blocking on result is common — parallelism is not necessarily needed!

Alright, so how should we use threading? Python `threading` library is a possibility. The threading library spawns OS threads, which are managed and scheduled by the OS. On Linux, this means that you'll use POSIX threads. This also means that your threads will be preemptively scheduled. Because of the [GIL](https://tenthousandmeters.com/blog/python-behind-the-scenes-13-the-gil-and-its-effects-on-python-multithreading/), a scheduled and running thread may end up immediately yielding because they do not have the lock (the attached link is really good). Another downside is that OS level threads can be [expensive](https://stackoverflow.com/questions/9964899/why-are-os-threads-considered-expensive) to create (TODO: potentially evaluate the slowdown). This is a commonly-cited reason for not using `threading`, even when using a [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor) (I'm assuming this works by maintaining a list of threads which pick tasks off of a queue). Some reasons include:

- Context switching can be expensive. It looks like this takes around [10](https://github.com/sirupsen/napkin-math) microseconds, but possibly higher with Python overhead.
- Acquiring the GIL can take several cycles (I don’t have a fermi estimate for this)
- Thread memory needs to be created

The alternative is to consider collaborative multitasking. At the time of writing this, there are two common approaches: [asyncio](https://docs.python.org/3/library/asyncio.html) and and [green threads](https://www.gevent.org/).