import time

def fetch_data(id):
    print(f"Task {id} starting...")
    time.sleep(2)  # Simulates a heavy I/O bound task (like an API call)
    print(f"Task {id} finished!")


def main():
    start_time = time.perf_counter()

    for i in range(1, 4):
        fetch_data(i)

    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time:.2f} seconds")


main()

import asyncio
import time

async def fetch_data_async(id):
    print(f"Task {id} starting...")
    await asyncio.sleep(2)  # Non-blocking wait
    print(f"Task {id} finished!")

async def main():
    start_time = time.perf_counter()

    # Schedule all tasks to run concurrently
    tasks = [fetch_data_async(i) for i in range(1, 4)]
    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time:.2f} seconds")

asyncio.run(main())