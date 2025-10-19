import os
import re

class JavaHandler:
    def generate(self, code, output_path, index):
        # 从代码中提取类名
        class_name = self._extract_class_name(code)
        if not class_name:
            raise XfawaError("Java code must contain a public class", None)
        
        filename = f"{class_name}.java"
        filepath = os.path.join(output_path, filename)
        
        # 生成Java文件
        with open(filepath, 'w') as f:
            f.write(code)
        
        # 返回块信息
        return {
            'id': f"block_{index}",
            'filename': filename,
            'filepath': filepath,
            'class_name': class_name,
            'block_ref': class_name
        }
    
    def _extract_class_name(self, code):
        # 简单匹配public class
        match = re.search(r'public\s+class\s+(\w+)', code)
        if match:
            return match.group(1)
        return None
