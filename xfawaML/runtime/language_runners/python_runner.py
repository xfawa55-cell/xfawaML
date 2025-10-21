import sys
import importlib
from ..xfawa_runtime import XfawaRuntime

def run_python(module_name, function_name):
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, function_name)
        return func()
    except Exception as e:
        print(f"Python runner error: {str(e)}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python python_runner.py <module> <function>")
        sys.exit(1)
    
    module = sys.argv[1]
    function = sys.argv[2]
    result = run_python(module, function)
    if result is not None:
        print(result)
