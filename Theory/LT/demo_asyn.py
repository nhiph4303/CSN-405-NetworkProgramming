import asyncio

# async def worker(n):
#     print(f"Worker {n} started")
#     await asyncio.sleep(2)  
#     print(f"Worker {n} finished")

async def task1():
    print("Task 1 started")
    await asyncio.sleep(2)  
    print("Task 1 completed")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(0.5)  
    print("Task 2 completed")

async def main():
    # task = [worker(i) for i in range(4)]
     
    # print("Hello")
    # await asyncio.sleep(10)
    # print("World")

    await asyncio.gather(task1(), task2())

asyncio.run(main())