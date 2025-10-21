import os

class GoHandler:
    def generate(self, code, output_path, index):
        filename = f"go_block_{index}.go"
        filepath = os.path.join(output_path, filename)
        exe_path = os.path.join(output_path, f"go_block_{index}")
        
        # 生成Go文件
        with open(filepath, 'w') as f:
            f.write("package main\n\n")
            f.write("import \"fmt\"\n\n")
            f.write("func main() {\n")
            for line in code.split('\n'):
                f.write(f"    {line}\n")
            f.write("}\n")
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'exe_path': exe_path,
            'block_ref': exe_path
        }
