import os

class CppHandler:
    def generate(self, code, output_path, index):
        filename = f"cpp_block_{index}.cpp"
        filepath = os.path.join(output_path, filename)
        exe_path = os.path.join(output_path, f"cpp_block_{index}")
        
        # 生成C++文件
        with open(filepath, 'w') as f:
            f.write("#include <iostream>\n")
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
