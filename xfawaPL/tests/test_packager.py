import unittest
import os
import shutil
from packager.linux import LinuxPackager
from compiler.parser import XfawaParser
from compiler.code_generator import CodeGenerator

class TestPackager(unittest.TestCase):
    def setUp(self):
        self.dist_dir = "test_dist"
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
        os.makedirs(self.dist_dir)
        
    def tearDown(self):
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
    
    def test_linux_package(self):
        # 创建一个模拟的构建目录结构
        build_dir = os.path.join(self.dist_dir, "build")
        os.makedirs(build_dir)
        
        # 创建一些模拟文件
        with open(os.path.join(build_dir, "entry.py"), 'w') as f:
            f.write("print('Hello')")
        
        # 模拟构建数据
        build_data = {
            'build_dir': build_dir,
            'entry_file': os.path.join(build_dir, "entry.py"),
            'dockerfile': os.path.join(build_dir, "Dockerfile"),
            'build_script': os.path.join(build_dir, "build.sh"),
            'file_map': {
                'Python': [{'filepath': os.path.join(build_dir, "python", "python_block_0.py")}]
            }
        }
        
        # 创建build.sh
        with open(build_data['build_script'], 'w') as f:
            f.write("echo 'Build script'")
        os.chmod(build_data['build_script'], 0o755)
        
        # 创建Dockerfile
        with open(build_data['dockerfile'], 'w') as f:
            f.write("FROM alpine\nCOPY . /app")
        
        # 打包
        packager = LinuxPackager()
        output_path = packager.package(build_data, "test_app")
        
        # 检查输出文件是否存在
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.tar.gz'))

if __name__ == '__main__':
    unittest.main()
