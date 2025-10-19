import os
import tarfile
from .common import BasePackager

class LinuxPackager(BasePackager):
    def create_launch_script(self, app_dir, output_name):
        script_path = os.path.join(app_dir, output_name)
        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write(f"cd {os.path.dirname(__file__)}\n")
            f.write("python3 -m runtime.xfawa_runtime\n")
        os.chmod(script_path, 0o755)
    
    def create_archive(self, app_dir, output_name):
        archive_path = os.path.join('dist', f'{output_name}.tar.gz')
        with tarfile.open(archive_path, 'w:gz') as tar:
            tar.add(app_dir, arcname=output_name)
        return archive_path
