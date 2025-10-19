import os

class CHandler:
    def generate(self, code, output_path, index):
        filename = f"c_block_{index}.c"
        filepath = os.path.join(output_path, filename)
        exe_path = os.path.join(output_path, f"c_block_{index}")
        
        # 生成C文件
        with open(filepath, 'w') as f:
            f.write("#include <stdio.h>\n")
            f.write("int main() {\n")
            for line in code.split('\n'):
                f.write(f"    {line}\n")
            f.write("    return 0;\n")
            f.write("}\n")
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'exe_path': exe_path,
            'block_ref': exe_path
        }
