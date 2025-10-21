import re
import json
from .error_handler import XfawaError

class XfawaParser:
    def __init__(self, source_code, file_path):
        self.source_code = source_code
        self.file_path = file_path
        self.blocks = {}
        self.data = {
            'define_output': False,  # 默认不启用强制Main块控制
            'entry_point': None
        }
        
    def parse(self):
        # 解析所有代码块
        pattern = r'#(\w+)\s*\[\[(.*?)\]\]\s*(?=#|$)'
        matches = re.findall(pattern, self.source_code, re.DOTALL)
        
        for block_type, content in matches:
            block_type = block_type.lower().strip()
            content = content.strip()
            
            if block_type == 'data':
                self._parse_data(content)
            else:
                if block_type not in self.blocks:
                    self.blocks[block_type] = []
                self.blocks[block_type].append(content)
        
        return {
            'blocks': self.blocks,
            'data': self.data
        }
    
    def _parse_data(self, content):
        try:
            data = json.loads(content)
            if 'Define_Output' in data:
                self.data['define_output'] = data['Define_Output']
            if 'Entry_Point' in data:
                self.data['entry_point'] = data['Entry_Point']
        except json.JSONDecodeError:
            raise XfawaError("Invalid data format", self.file_path)
