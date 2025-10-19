import unittest
import os
import subprocess
from runtime.xfawa_runtime import XfawaRuntime

class TestRuntime(unittest.TestCase):
    def test_python_runtime(self):
        runtime = XfawaRuntime()
        runtime.init_env('python')
        
        # 创建一个临时的Python模块
        os.makedirs('test_python', exist_ok=True)
        with open('test_python/test_func.py', 'w') as f:
            f.write("def main():\n    return 'Hello from Python'")
        
        # 注册并运行代码块
        runtime.register_block('python', 'test_block', 'test_python.test_func.main')
        result = runtime.run('python', 'test_block')
        self.assertEqual(result, 'Hello from Python')
        
        shutil.rmtree('test_python')
    
    def test_c_runtime(self):
        runtime = XfawaRuntime()
        runtime.init_env('c')
        
        # 创建一个临时的C文件并编译
        with open('test_c.c', 'w') as f:
            f.write("#include <stdio.h>\n")
            f.write("int main() {\n")
            f.write("    printf(\"Hello from C\\n\");\n")
            f.write("    return 0;\n")
            f.write("}\n")
        
        # 编译
        subprocess.run(['gcc', 'test_c.c', '-o', 'test_c'], check=True)
        
        # 注册并运行代码块
        runtime.register_block('c', 'test_block', os.path.abspath('test_c'))
        result = runtime.run('c', 'test_block')
        self.assertIn('Hello from C', result)
        
        os.remove('test_c.c')
        os.remove('test_c')

if __name__ == '__main__':
    unittest.main()
