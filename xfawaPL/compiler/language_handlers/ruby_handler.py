import os

class RubyHandler:
    def generate(self, code, output_path, index):
        filename = f"ruby_block_{index}.rb"
        filepath = os.path.join(output_path, filename)
        
        # 生成Ruby文件
        with open(filepath, 'w') as f:
            f.write("def main\n")
            for line in code.split('\n'):
                f.write(f"    {line}\n")
            f.write("end\n")
            f.write("main\n")
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'block_ref': filepath
        }
