import os

class ShellHandler:
    def generate(self, code, output_path, index):
        filename = f"shell_block_{index}.sh"
        filepath = os.path.join(output_path, filename)
        
        # 生成Shell脚本
        with open(filepath, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("function main() {\n")
            for line in code.split('\n'):
                f.write(f"    {line}\n")
            f.write("}\n")
            f.write("main\n")
        
        # 设置可执行权限
        os.chmod(filepath, 0o755)
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'block_ref': filepath
        }
