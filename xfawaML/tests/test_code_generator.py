import unittest
import os
import shutil
from compiler.parser import XfawaParser
from compiler.code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.build_dir = "test_build"
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)
        
    def tearDown(self):
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
    
    def test_generate_with_main(self):
        source = """
#Python [[
print("Hello Python")
]]

#C [[
#include <stdio.h>
int main() {
    printf("Hello C\\n");
    return 0;
}
]]

#Main [[
xfawa.run("C")
xfawa.run("Python")
]]

#data [[
{
    "Define_Output": true
}
]]
"""
        parser = XfawaParser(source, "test.xf")
        parsed_data = parser.parse()
        
        generator = CodeGenerator(self.build_dir)
        build_data = generator.generate(parsed_data, "test_app")
        
        self.assertTrue(os.path.exists(build_data['entry_file']))
        self.assertTrue(os.path.exists(build_data['dockerfile']))
        self.assertTrue(os.path.exists(build_data['build_script']))
        
        # 检查Python文件是否生成
        py_files = build_data['file_map']['Python']
        self.assertEqual(len(py_files), 1)
        self.assertTrue(os.path.exists(py_files[0]['filepath']))
        
        # 检查C文件是否生成
        c_files = build_data['file_map']['C']
        self.assertEqual(len(c_files), 1)
        self.assertTrue(os.path.exists(c_files[0]['filepath']))
        
        # 检查构建脚本中是否有编译C的命令
        with open(build_data['build_script'], 'r') as f:
            build_script = f.read()
            self.assertIn('gcc', build_script)
    
    def test_generate_without_main(self):
        source = """
#Python [[
print("Hello Python")
]]

#Shell [[
echo "Hello from Shell"
]]

#data [[
{
    "Define_Output": false
}
]]
"""
        parser = XfawaParser(source, "test.xf")
        parsed_data = parser.parse()
        
        generator = CodeGenerator(self.build_dir)
        build_data = generator.generate(parsed_data, "test_app")
        
        self.assertTrue(os.path.exists(build_data['entry_file']))
        self.assertTrue(os.path.exists(build_data['dockerfile']))
        self.assertTrue(os.path.exists(build_data['build_script']))
        
        # 检查入口文件是否包含自动执行逻辑
        with open(build_data['entry_file'], 'r') as f:
            entry_code = f.read()
            self.assertIn('runtime.run', entry_code)

if __name__ == '__main__':
    unittest.main()
