import os

class JavaScriptHandler:
    def generate(self, code, output_path, index):
        filename = f"js_block_{index}.js"
        filepath = os.path.join(output_path, filename)
        
        # 生成JavaScript文件
        with open(filepath, 'w') as f:
            f.write("function main() {\n")
            for line in code.split('\n'):
                f.write(f"    {line}\n")
            f.write("}\n")
            f.write("main();\n")
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'block_ref': filepath
        }
