import time
import threading
import multiprocessing

def cpu_heavy_task(n=10_000_000):
    """A task that keeps the CPU busy."""
    # count = 0
    # for i in range(n):
    #     count += i**2
    # return count
    time.sleep(5)

def run_test(name, type='sequential'):
    start_time = time.perf_counter()

    if type == 'sequential':
        for _ in range(4):
            cpu_heavy_task()

    elif type == 'threading':
        threads = []
        for _ in range(4):
            t = threading.Thread(target=cpu_heavy_task)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    elif type == 'multiprocessing':
        processes = []
        for _ in range(4):
            p = multiprocessing.Process(target=cpu_heavy_task)
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

    end_time = time.perf_counter()
    print(f"{name:15} | Time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    print("Running CPU-bound tasks (4 iterations):")
    print("-" * 40)
    run_test("Sequential", 'sequential')
    run_test("Multi-threading", 'threading')
    run_test("Multi-process", 'multiprocessing')