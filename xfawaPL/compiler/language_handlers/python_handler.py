import os

class PythonHandler:
    def generate(self, code, output_path, index):
        # 生成唯一的模块名
        module_name = f"python_block_{index}"
        filename = f"{module_name}.py"
        filepath = os.path.join(output_path, filename)
        
        # 生成Python文件
        with open(filepath, 'w') as f:
            f.write("def main():\n")
            for line in code.split('\n'):
                f.write(f"    {line}\n")
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'block_ref': f"{module_name}.main"
        }
