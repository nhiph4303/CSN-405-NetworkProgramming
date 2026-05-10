import time
import asyncio


async def fetch_data(id):
    print(f"Task {id} starting...")
    await asyncio.sleep(2)
    print(f"Task {id} completed.")


async def main():
    start_time = time.perf_counter()

    tasks = [fetch_data(i) for i in range(1, 4)]
    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    print(f"Total time {end_time - start_time:.10f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())