import os
import shutil
import zipfile

class XfawaPacker:
    @staticmethod
    def create_zip(output_path="xfawaPL.zip"):
        with zipfile.ZipFile(output_path, 'w') as zipf:
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith(('.py', '.xf', '.md')):
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, '.')
                        zipf.write(full_path, arcname)
        return output_path

    @staticmethod
    def create_standalone(output_dir="dist"):
        os.makedirs(output_dir, exist_ok=True)
        for item in ['xfawa.py', 'demo.xf', 'README.md']:
            if os.path.exists(item):
                shutil.copy2(item, output_dir)
        return output_dir
