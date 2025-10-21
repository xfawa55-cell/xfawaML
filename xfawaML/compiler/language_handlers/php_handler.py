import os

class PHPHandler:
    def generate(self, code, output_path, index):
        filename = f"php_block_{index}.php"
        filepath = os.path.join(output_path, filename)
        
        # 生成PHP文件
        with open(filepath, 'w') as f:
            f.write("<?php\n")
            f.write("function main() {\n")
            for line in code.split('\n'):
                f.write(f"    {line}\n")
            f.write("}\n")
            f.write("main();\n")
            f.write("?>\n")
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'block_ref': filepath
        }
