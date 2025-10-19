import os
import zipfile
import subprocess
from .common import BasePackager
from compiler.error_handler import XfawaError

class WindowsPackager(BasePackager):
    def create_launch_script(self, app_dir, output_name):
        # 创建批处理文件
        bat_path = os.path.join(app_dir, f"{output_name}.bat")
        with open(bat_path, 'w') as f:
            f.write("@echo off\n")
            f.write(f"cd {os.path.dirname(__file__)}\n")
            f.write("python -m runtime.xfawa_runtime\n")
            f.write("pause\n")
        
        # 创建PowerShell脚本
        ps_path = os.path.join(app_dir, f"{output_name}.ps1")
        with open(ps_path, 'w') as f:
            f.write("Set-Location -Path $PSScriptRoot\n")
            f.write("python -m runtime.xfawa_runtime\n")
            f.write("Read-Host -Prompt 'Press Enter to continue'\n")
    
    def create_archive(self, app_dir, output_name):
        archive_path = os.path.join('dist', f'{output_name}.zip')
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(app_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, app_dir)
                    zipf.write(file_path, arcname=os.path.join(output_name, arcname))
        return archive_path
    
    def create_exe(self, app_dir, output_name):
        """使用PyInstaller创建Windows可执行文件"""
        try:
            # 创建spec文件
            spec_content = f"""
# {output_name}.spec
import sys
from PyInstaller.building.build_main import Analysis, EXE, COLLECT

a = Analysis(
    ['{os.path.join(app_dir, 'entry.py')}'],
    pathex=['{app_dir}'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None
)

exe = EXE(
    a,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='{output_name}',
    debug=False,
    strip=False,
    upx=True,
    console=True,
    icon=None
)
"""
            spec_path = os.path.join(app_dir, f"{output_name}.spec")
            with open(spec_path, 'w') as f:
                f.write(spec_content)
            
            # 运行PyInstaller
            subprocess.run(['pyinstaller', '--onefile', spec_path], check=True)
            
            # 移动生成的可执行文件
            exe_src = os.path.join('dist', f"{output_name}.exe")
            exe_dst = os.path.join('dist', f"{output_name}.exe")
            shutil.move(exe_src, exe_dst)
            
            return exe_dst
        except Exception as e:
            raise XfawaError(f"Failed to create Windows executable: {str(e)}")
    
    def package(self, build_data, output_name):
        archive_path = super().package(build_data, output_name)
        exe_path = self.create_exe(os.path.join('dist', output_name), output_name)
        return exe_path
