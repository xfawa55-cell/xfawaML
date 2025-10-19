import os
import importlib
import re
from .error_handler import XfawaError

class CodeGenerator:
    LANGUAGE_HANDLERS = {
        'python': 'PythonHandler',
        'c': 'CHandler',
        'cpp': 'CppHandler',
        'java': 'JavaHandler',
        'go': 'GoHandler',
        'javascript': 'JavaScriptHandler',
        'lua': 'LuaHandler',
        'ruby': 'RubyHandler',
        'php': 'PHPHandler',
        'shell': 'ShellHandler'
    }
    
    def __init__(self, build_dir='build'):
        self.build_dir = build_dir
        os.makedirs(build_dir, exist_ok=True)
        self.handlers = {}
        self._load_handlers()
        
    def _load_handlers(self):
        for lang, handler_name in self.LANGUAGE_HANDLERS.items():
            module = importlib.import_module(f'.language_handlers.{lang}_handler', package='compiler')
            handler_class = getattr(module, handler_name)
            self.handlers[lang] = handler_class()
    
    def generate(self, parsed_data, output_name):
        blocks = parsed_data['blocks']
        data = parsed_data['data']
        define_output = data['define_output']
        
        # 检查强制Main块控制
        if define_output and 'main' not in blocks:
            raise XfawaError("Define_Output is true but no main block found", "")
        
        # 创建语言目录
        for lang in blocks.keys():
            if lang != 'main':  # Main块不需要目录
                lang_dir = os.path.join(self.build_dir, lang)
                os.makedirs(lang_dir, exist_ok=True)
        
        # 生成所有语言块代码
        file_map = {}
        for lang, code_list in blocks.items():
            if lang == 'main':  # Main块单独处理
                continue
                
            if lang not in self.handlers:
                raise XfawaError(f"Unsupported language: {lang}", "")
                
            handler = self.handlers[lang]
            file_map[lang] = []
            
            for i, code in enumerate(code_list):
                file_info = handler.generate(code, os.path.join(self.build_dir, lang), i)
                file_map[lang].append(file_info)
        
        # 生成入口文件
        entry_file = None
        if 'main' in blocks:
            entry_file = self._generate_entry_file(blocks['main'][0], file_map)
        else:
            entry_file = self._generate_default_entry_file(file_map)
        
        # 生成Dockerfile
        dockerfile = self._generate_dockerfile(file_map.keys())
        dockerfile_path = os.path.join(self.build_dir, 'Dockerfile')
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile)
        
        # 生成构建脚本
        build_script = self._generate_build_script(file_map)
        build_script_path = os.path.join(self.build_dir, 'build.sh')
        with open(build_script_path, 'w') as f:
            f.write(build_script)
        os.chmod(build_script_path, 0o755)
        
        return {
            'build_dir': self.build_dir,
            'entry_file': entry_file,
            'dockerfile': dockerfile_path,
            'build_script': build_script_path,
            'file_map': file_map,
            'define_output': define_output
        }
    
    def _generate_entry_file(self, main_code, file_map):
        """生成入口文件（当存在Main块时）"""
        entry_file = os.path.join(self.build_dir, 'entry.py')
        
        # 解析Main块中的xfawa.run调用顺序
        run_calls = self._parse_run_calls(main_code)
        
        with open(entry_file, 'w') as f:
            f.write("from runtime.xfawa_runtime import XfawaRuntime\n")
            f.write("import os\n\n")
            f.write("def main():\n")
            f.write("    runtime = XfawaRuntime()\n")
            
            # 添加各语言环境初始化
            for lang in file_map:
                f.write(f"    runtime.init_{lang}_env()\n")
            
            # 注册所有代码块
            f.write("\n    # Register code blocks\n")
            for lang, blocks in file_map.items():
                for i, block in enumerate(blocks):
                    f.write(f"    runtime.register_block('{lang}', 'block_{i}', '{block['block_ref']}')\n")
            
            # 按照Main块中的调用顺序执行
            f.write("\n    # Execute blocks in priority order\n")
            for lang in run_calls:
                if lang in file_map:
                    for i in range(len(file_map[lang])):
                        f.write(f"    runtime.run('{lang}', 'block_{i}')\n")
                else:
                    f.write(f"    # Warning: Language '{lang}' not found\n")
            
            f.write("\nif __name__ == '__main__':\n")
            f.write("    main()\n")
        
        return entry_file
    
    def _parse_run_calls(self, main_code):
        """解析Main块中的xfawa.run调用顺序"""
        pattern = r'xfawa\.run\("(\w+)"\)'
        matches = re.findall(pattern, main_code)
        return matches
    
    def _generate_default_entry_file(self, file_map):
        """生成默认入口文件（当没有Main块时）"""
        entry_file = os.path.join(self.build_dir, 'entry.py')
        
        with open(entry_file, 'w') as f:
            f.write("from runtime.xfawa_runtime import XfawaRuntime\n")
            f.write("import os\n\n")
            f.write("def main():\n")
            f.write("    runtime = XfawaRuntime()\n")
            
            # 添加各语言环境初始化
            for lang in file_map:
                f.write(f"    runtime.init_{lang}_env()\n")
            
            # 注册所有代码块
            f.write("\n    # Register code blocks\n")
            for lang, blocks in file_map.items():
                for i, block in enumerate(blocks):
                    f.write(f"    runtime.register_block('{lang}', 'block_{i}', '{block['block_ref']}')\n")
            
            # 按源文件顺序执行所有语言块
            f.write("\n    # Execute all blocks\n")
            for lang, blocks in file_map.items():
                for i in range(len(blocks)):
                    f.write(f"    runtime.run('{lang}', 'block_{i}')\n")
            
            f.write("\nif __name__ == '__main__':\n")
            f.write("    main()\n")
        
        return entry_file
    
    def _generate_dockerfile(self, languages):
        """生成Dockerfile"""
        dockerfile = "FROM ubuntu:20.04\n\n"
        dockerfile += "# 安装基本工具 Basic tools for installation\n"
        dockerfile += "RUN apt-get update && apt-get install -y \\\n"
        dockerfile += "    python3 \\\n"
        dockerfile += "    python3-pip \\\n"
        dockerfile += "    gcc \\\n"
        dockerfile += "    g++ \\\n"
        dockerfile += "    openjdk-11-jdk \\\n"
        dockerfile += "    nodejs \\\n"
        dockerfile += "    npm \\\n"
        dockerfile += "    golang \\\n"
        dockerfile += "    lua5.3 \\\n"
        dockerfile += "    ruby \\\n"
        dockerfile += "    php \\\n"
        dockerfile += "    && rm -rf /var/lib/apt/lists/*\n\n"
        dockerfile += "WORKDIR /app\n"
        dockerfile += "COPY . /app\n\n"
        dockerfile += "RUN chmod +x build.sh\n"
        dockerfile += "RUN ./build.sh\n\n"
        dockerfile += 'CMD ["python3", "entry.py"]'
        
        return dockerfile
    
    def _generate_build_script(self, file_map):
        """生成构建脚本"""
        script = "#!/bin/bash\n\n"
        script += "echo 'Building xfawaPL application...'\n\n"
        
        # 编译各语言代码
        for lang, files in file_map.items():
            for file_info in files:
                if lang == 'c':
                    script += f"gcc {file_info['filepath']} -o {file_info['exe_path']}\n"
                elif lang == 'cpp':
                    script += f"g++ {file_info['filepath']} -o {file_info['exe_path']}\n"
                elif lang == 'java':
                    script += f"javac {file_info['filepath']}\n"
                elif lang == 'go':
                    script += f"go build -o {file_info['exe_path']} {file_info['filepath']}\n"
        
        script += "\necho 'Build completed successfully!'\n"
        return script
