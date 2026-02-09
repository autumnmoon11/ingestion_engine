import functools
import time
import logging

logger = logging.getLogger(__name__)

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

        # Store the telemetry data (State)
        wrapper.last_execution_time = execution_time
        
        # 2. Log the event (Observation)
        logger.info(f"Execution: {func.__name__} | Time: {execution_time:.4f}s")

        # Decorator must always return the result of the original function to maintain 
        # transparency for the caller.
        return result
    return wrapper