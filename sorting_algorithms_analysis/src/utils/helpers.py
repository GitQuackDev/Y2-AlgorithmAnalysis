
import time
import random
from typing import List, Callable, Any

def time_function(func: Callable, *args, **kwargs) -> tuple:
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    
    return result, end_time - start_time

def is_sorted(arr: List[int]) -> bool:
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

def generate_random_array(size: int, min_val: int = 0, max_val: int = None) -> List[int]:
    if max_val is None:
        max_val = size * 10
    
    return [random.randint(min_val, max_val) for _ in range(size)]

def format_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.3f} s"

def calculate_statistics(times: List[float]) -> dict:
    if not times:
        return {}
    
    mean_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    
    variance = sum((t - mean_time) ** 2 for t in times) / len(times)
    std_dev = variance ** 0.5
    
    return {
        'mean': mean_time,
        'min': min_time,
        'max': max_time,
        'std_dev': std_dev,
        'count': len(times)
    }
