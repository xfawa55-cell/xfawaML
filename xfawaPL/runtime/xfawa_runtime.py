import subprocess
import os
import sys
import importlib
import ctypes

class XfawaRuntime:
    def __init__(self):
        self.language_envs = {}
        self.block_registry = {}  # 存储注册的代码块
    
    def init_env(self, language):
        """初始化指定语言环境"""
        if language == 'python':
            self.init_python_env()
        elif language == 'c':
            self.init_c_env()
        elif language == 'cpp':
            self.init_cpp_env()
        elif language == 'java':
            self.init_java_env()
        elif language == 'go':
            self.init_go_env()
        elif language == 'javascript':
            self.init_javascript_env()
        elif language == 'lua':
            self.init_lua_env()
        elif language == 'ruby':
            self.init_ruby_env()
        elif language == 'php':
            self.init_php_env()
        elif language == 'shell':
            self.init_shell_env()
        else:
            raise RuntimeError(f"Unsupported language: {language}")
    
    def register_block(self, language, block_id, block_ref):
        """注册代码块"""
        if language not in self.block_registry:
            self.block_registry[language] = {}
        self.block_registry[language][block_id] = block_ref
    
    def run(self, language, block_id):
        """
        运行指定语言的代码块
        :param language: 语言名称
        :param block_id: 代码块ID
        """
        if language not in self.language_envs:
            self.init_env(language)
        
        if language in self.block_registry and block_id in self.block_registry[language]:
            return self.language_envs[language]['run_block'](self.block_registry[language][block_id])
        else:
            raise RuntimeError(f"Block {block_id} not found for language {language}")
    
    # Python环境
    def init_python_env(self):
        self.language_envs['python'] = {
            'run_block': self._run_python_block
        }
    
    def _run_python_block(self, block_ref):
        """运行特定Python代码块"""
        module_name, func_name = block_ref.split('.')
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        return func()
    
    # C环境
    def init_c_env(self):
        self.language_envs['c'] = {
            'run_block': self._run_c_block
        }
    
    def _run_c_block(self, block_ref):
        """运行特定C代码块"""
        exe_path = block_ref
        result = subprocess.run([exe_path], capture_output=True, text=True)
        return result.stdout
    
    # C++环境
    def init_cpp_env(self):
        self.language_envs['cpp'] = {
            'run_block': self._run_cpp_block
        }
    
    def _run_cpp_block(self, block_ref):
        """运行特定C++代码块"""
        exe_path = block_ref
        result = subprocess.run([exe_path], capture_output=True, text=True)
        return result.stdout
    
    # Java环境
    def init_java_env(self):
        self.language_envs['java'] = {
            'run_block': self._run_java_block
        }
    
    def _run_java_block(self, block_ref):
        """运行特定Java代码块"""
        class_name = block_ref
        class_path = os.path.join('build', 'java')
        result = subprocess.run(
            ['java', '-cp', class_path, class_name],
            capture_output=True, text=True
        )
        return result.stdout
    
    # Go环境
    def init_go_env(self):
        self.language_envs['go'] = {
            'run_block': self._run_go_block
        }
    
    def _run_go_block(self, block_ref):
        """运行特定Go代码块"""
        exe_path = block_ref
        result = subprocess.run([exe_path], capture_output=True, text=True)
        return result.stdout
    
    # JavaScript环境
    def init_javascript_env(self):
        self.language_envs['javascript'] = {
            'run_block': self._run_javascript_block
        }
    
    def _run_javascript_block(self, block_ref):
        """运行特定JavaScript代码块"""
        script_path = block_ref
        result = subprocess.run(['node', script_path], capture_output=True, text=True)
        return result.stdout
    
    # Lua环境
    def init_lua_env(self):
        self.language_envs['lua'] = {
            'run_block': self._run_lua_block
        }
    
    def _run_lua_block(self, block_ref):
        """运行特定Lua代码块"""
        script_path = block_ref
        result = subprocess.run(['lua', script_path], capture_output=True, text=True)
        return result.stdout
    
    # Ruby环境
    def init_ruby_env(self):
        self.language_envs['ruby'] = {
            'run_block': self._run_ruby_block
        }
    
    def _run_ruby_block(self, block_ref):
        """运行特定Ruby代码块"""
        script_path = block_ref
        result = subprocess.run(['ruby', script_path], capture_output=True, text=True)
        return result.stdout
    
    # PHP环境
    def init_php_env(self):
        self.language_envs['php'] = {
            'run_block': self._run_php_block
        }
    
    def _run_php_block(self, block_ref):
        """运行特定PHP代码块"""
        script_path = block_ref
        result = subprocess.run(['php', script_path], capture_output=True, text=True)
        return result.stdout
    
    # Shell环境
    def init_shell_env(self):
        self.language_envs['shell'] = {
            'run_block': self._run_shell_block
        }
    
    def _run_shell_block(self, block_ref):
        """运行特定Shell代码块"""
        script_path = block_ref
        result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        return result.stdout
