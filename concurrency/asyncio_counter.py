import asyncio

# silly example where we maintain a local and global counter, the latter is incremented across 
# async tasks.

class _Counter:
    _CLS_COUNTER = 0 
    def __init__(self) -> None:
        self.count = 0 

    def inc(self):
        self.count += 1 
        _Counter._CLS_COUNTER += 1


async def run_counter():
    c = _Counter()

    for _ in range(10):
        await asyncio.sleep(0.1)
        c.inc()
    print(c.count)

async def main():
    await asyncio.gather(*(run_counter() for _ in range(10)))

asyncio.run(main())
print(_Counter._CLS_COUNTER)
