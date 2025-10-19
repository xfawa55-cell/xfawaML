import os
import shutil
import tarfile
import zipfile
import subprocess
from compiler.error_handler import XfawaError

class BasePackager:
    def __init__(self):
        self.runtime_files = [
            'xfawa_runtime.py',
            'language_runners'
        ]
    
    def copy_runtime_files(self, app_dir):
        """复制运行时文件到应用目录"""
        runtime_src = os.path.dirname(os.path.abspath(__file__))
        runtime_src = os.path.join(runtime_src, '..', 'runtime')
        
        for file in self.runtime_files:
            src = os.path.join(runtime_src, file)
            dst = os.path.join(app_dir, file)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
    
    def create_launch_script(self, app_dir, output_name):
        """创建启动脚本（子类实现）"""
        raise NotImplementedError
    
    def create_archive(self, app_dir, output_name):
        """创建压缩包（子类实现）"""
        raise NotImplementedError
    
    def package(self, build_data, output_name):
        """打包应用"""
        build_dir = build_data['build_dir']
        
        # 创建应用目录
        app_dir = os.path.join('dist', output_name)
        os.makedirs(app_dir, exist_ok=True)
        
        # 复制运行时文件
        self.copy_runtime_files(app_dir)
        
        # 复制构建文件
        shutil.copytree(build_dir, os.path.join(app_dir, 'build'))
        
        # 创建启动脚本
        self.create_launch_script(app_dir, output_name)
        
        # 创建压缩包
        archive_path = self.create_archive(app_dir, output_name)
        
        return archive_path
