import asyncio
import time

async def task(name, delay):
    print(f"{name} start")
    await asyncio.sleep(delay)
    print(f"{name} end")

async def main():
    start = time.time()

    await asyncio.gather(
        task("A", 1),
        task("B", 4),
        task("C", 3)
    )

    total = time.time() - start
    print(f"Total time: {total:.2f}s")

asyncio.run(main())
