import functools
import time

# Decorator: A Higher-Order Function that accepts a function as an 
# argument and returns a new function with extended behavior.
def time_execution_decorator(func):
    # 'Metadata Preserver': Ensures the decorated function keeps its original __name__ and docstring.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_function_time = time.perf_counter()
        # Execute the 'wrapped' function and store its return value in 'result'
        result = func(*args, **kwargs)
        end_function_time = time.perf_counter()
        execution_time = end_function_time - start_function_time
        print(f"Function {func.__name__} took {execution_time:.6f} seconds to execute.")
        # Decorator must always return the result of the original function to maintain 
        # transparency for the caller.
        return result
    return wrapper

# Pie Syntax - equivalent to: heavy_computation = time_execution_decorator(heavy_computation)
@time_execution_decorator
def heavy_computation(duration: int):
    """Simulates a long-running process."""
    time.sleep(duration)
    return "Task Complete"

if __name__ == "__main__":
    status = heavy_computation(2)
    print(f"Result: {status}")