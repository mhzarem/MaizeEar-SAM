import os
import time
import psutil
import tracemalloc


def resource_usage_decorator(func):
    def wrapped_func(*args, **kwargs):
        process = psutil.Process(os.getpid())
        cpu_percent_before = process.cpu_percent(interval=None)
        tracemalloc.start()  # Start tracing memory allocations
        num_cores = psutil.cpu_count()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        current, peak = tracemalloc.get_traced_memory()  # Get memory usage
        tracemalloc.stop()  # Stop tracing memory allocations
        cpu_percent_after = process.cpu_percent(interval=None)

        time_elapsed = end_time - start_time
        mem_used = current
        cpu_percent_used = cpu_percent_after - cpu_percent_before

        print(f"{func.__name__} took {time_elapsed:.4f} seconds")
        #print(f"{func.__name__} used {mem_used /(1024*1024):.2f} MB of memory")
        #print(f"{func.__name__} used {cpu_percent_used / num_cores:.2f}% of CPU")

        return result

    return wrapped_func
