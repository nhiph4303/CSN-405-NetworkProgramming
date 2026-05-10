import asyncio


async def worker(n):
    print(f"Worker {n} started")
    await asyncio.sleep(2)
    print(f"Worker {n} finished")


async def main():
    tasks = [asyncio.create_task(worker(i)) for i in range(5)]
    await asyncio.gather(*tasks)
