import subprocess
import tempfile
import os
import re
import shutil

class XfawaEngine:
    def __init__(self):
        self.variables = {}
        self.language_executors = {
            'python': self._exec_python,
            'bash': self._exec_bash,
            'shell': self._exec_bash,
            'sh': self._exec_bash,
            'lua': self._exec_lua,
            'c': self._exec_c,
            'cpp': self._exec_cpp,
            'c++': self._exec_cpp,
            'go': self._exec_go,
            'ruby': self._exec_ruby,
            'php': self._exec_php,
            'java': self._exec_java,
            'js': self._exec_javascript,
            'javascript': self._exec_javascript
        }

    def execute(self, command):
        command = command.strip()
        if not command or command.startswith('//'):
            return ""
        
        if ':=' in command:
            parts = command.split(':=', 1)
            if len(parts) == 2:
                key, value = parts[0].strip(), parts[1].strip()
                self.variables[key] = self._parse_value(value)
            return ""
        
        block_match = re.match(r'#(\w+)\s*\[\[(.*?)\]\]', command, re.DOTALL)
        if block_match:
            lang = block_match.group(1).lower()
            code = block_match.group(2).strip()
            
            for var_name, var_value in self.variables.items():
                code = code.replace(var_name, str(var_value))
            
            if lang in self.language_executors:
                return self.language_executors[lang](code)
            else:
                return f"Unsupported language: {lang}"
        
        return command

    def _parse_value(self, value):
        if value.isdigit():
            return int(value)
        elif value.replace('.', '').isdigit():
            return float(value)
        elif value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        elif (value.startswith('"') and value.endswith('"')) or \
             (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        else:
            return value

    def _exec_python(self, code):
        try:
            exec(code, {}, self.variables)
            return ""
        except Exception as e:
            return f"Python Error: {e}"

    def _exec_bash(self, code):
        try:
            result = subprocess.run(['bash', '-c', code], capture_output=True, text=True)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"Bash Error: {e}"

    def _exec_lua(self, code):
        try:
            result = subprocess.run(['lua', '-e', code], capture_output=True, text=True)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"Lua Error: {e}"

    def _exec_c(self, code):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                c_file = f.name
            
            exe_file = c_file.replace('.c', '.out')
            compile_result = subprocess.run(['gcc', c_file, '-o', exe_file], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return f"C Compile Error: {compile_result.stderr}"
            
            result = subprocess.run([exe_file], capture_output=True, text=True)
            os.unlink(c_file)
            os.unlink(exe_file)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"C Error: {e}"

    def _exec_cpp(self, code):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                f.write(code)
                cpp_file = f.name
            
            exe_file = cpp_file.replace('.cpp', '.out')
            compile_result = subprocess.run(['g++', cpp_file, '-o', exe_file], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return f"C++ Compile Error: {compile_result.stderr}"
            
            result = subprocess.run([exe_file], capture_output=True, text=True)
            os.unlink(cpp_file)
            os.unlink(exe_file)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"C++ Error: {e}"

    def _exec_go(self, code):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(code)
                go_file = f.name
            
            result = subprocess.run(['go', 'run', go_file], capture_output=True, text=True, timeout=30)
            os.unlink(go_file)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"Go Error: {e}"

    def _exec_ruby(self, code):
        try:
            result = subprocess.run(['ruby', '-e', code], capture_output=True, text=True)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"Ruby Error: {e}"

    def _exec_php(self, code):
        try:
            result = subprocess.run(['php', '-r', code], capture_output=True, text=True)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"PHP Error: {e}"

    def _exec_java(self, code):
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                f.write(code)
                java_file = f.name
            
            class_dir = tempfile.mkdtemp()
            compile_result = subprocess.run(['javac', '-d', class_dir, java_file], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return f"Java Compile Error: {compile_result.stderr}"
            
            class_name = "Main"
            if "class" in code:
                class_match = re.search(r'class\s+(\w+)', code)
                if class_match:
                    class_name = class_match.group(1)
            
            result = subprocess.run(['java', '-cp', class_dir, class_name], capture_output=True, text=True)
            os.unlink(java_file)
            shutil.rmtree(class_dir)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"Java Error: {e}"

    def _exec_javascript(self, code):
        try:
            result = subprocess.run(['node', '-e', code], capture_output=True, text=True)
            return result.stdout + (result.stderr if result.stderr else "")
        except Exception as e:
            return f"JavaScript Error: {e}"
