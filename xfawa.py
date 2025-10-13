#!/usr/bin/env python3

import sys
import os
import subprocess
import re
import tempfile
import shutil
from pathlib import Path
from threading import Timer

class XfawaSecurity:
    @staticmethod
    def validate_code(lang, code):
        dangerous_patterns = [
            r'__import__\s*\(', r'eval\s*\(', r'exec\s*\(', 
            r'os\.system', r'subprocess\.[a-zA-Z]', r'open\s*\([^)]*[w+a+]'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                raise Exception(f"Security risk: {pattern}")
        
        if lang == 'bash':
            if any(cmd in code for cmd in ['rm -rf', 'dd if=', 'mkfs', '> /dev/sd']):
                raise Exception("Dangerous system command detected")
    
    @staticmethod
    def safe_variable_replacement(code, variables):
        for var_name, var_value in variables.items():
            if isinstance(var_value, str):
                escaped_value = var_value.replace('"', '\\"').replace("'", "\\'")
                code = re.sub(r'\b' + re.escape(var_name) + r'\b', f'"{escaped_value}"', code)
            else:
                code = re.sub(r'\b' + re.escape(var_name) + r'\b', str(var_value), code)
        return code

class TempFileManager:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='xfawa_')
        self.file_cache = {}
    
    def create_temp_file(self, content, suffix):
        fd, path = tempfile.mkstemp(suffix=suffix, dir=self.temp_dir, text=True)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    def get_cached_binary(self, source_content, suffix, compile_cmd):
        content_hash = hash(source_content)
        if content_hash in self.file_cache:
            return self.file_cache[content_hash]
        
        source_path = self.create_temp_file(source_content, suffix)
        binary_path = source_path + '.out'
        
        try:
            subprocess.run(compile_cmd + [source_path, '-o', binary_path], check=True)
            self.file_cache[content_hash] = binary_path
            return binary_path
        except subprocess.CalledProcessError:
            raise
    
    def cleanup(self):
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

class XfawaEngine:
    def __init__(self, timeout=30, safe_mode=True):
        self.variables = {}
        self.is_mobile = os.path.exists('/data/data/com.termux/files/home')
        self.safe_mode = safe_mode
        self.timeout = timeout
        self.temp_manager = TempFileManager()
        self.executors = self._init_executors()
    
    def _init_executors(self):
        return {
            'python': (self._exec_python, '.py'),
            'bash': (self._exec_bash, '.sh'),
            'js': (self._exec_js, '.js'),
            'lua': (self._exec_lua, '.lua'),
            'c': (self._exec_compiled, ('.c', ['gcc'])),
            'cpp': (self._exec_compiled, ('.cpp', ['g++'])),
            'go': (self._exec_go, '.go'),
            'ruby': (self._exec_ruby, '.rb'),
            'php': (self._exec_php, '.php'),
            'java': (self._exec_java, '.java')
        }
    
    def _run_with_timeout(self, cmd, timeout=None):
        timeout = timeout or self.timeout
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return result
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Timeout after {timeout}s")
    
    def _exec_python(self, code):
        if self.safe_mode:
            XfawaSecurity.validate_code('python', code)
        
        safe_builtins = {'print': print, 'len': len, 'range': range, 'str': str, 'int': int}
        local_vars = self.variables.copy()
        exec(code, {'__builtins__': safe_builtins}, local_vars)
        
        for key, value in local_vars.items():
            if not key.startswith('_'):
                self.variables[key] = value
    
    def _exec_bash(self, code):
        if self.safe_mode:
            XfawaSecurity.validate_code('bash', code)
        
        script_path = self.temp_manager.create_temp_file(f"#!/bin/bash\n{code}", '.sh')
        os.chmod(script_path, 0o755)
        result = self._run_with_timeout(['bash', script_path])
        print(result.stdout, end='')
        if result.stderr:
            raise Exception(f"Bash: {result.stderr}")
    
    def _exec_compiled(self, code, lang_info):
        suffix, compiler = lang_info
        source_path = self.temp_manager.create_temp_file(code, suffix)
        
        try:
            binary_path = self.temp_manager.get_cached_binary(code, suffix, compiler)
            result = self._run_with_timeout([binary_path])
            print(result.stdout, end='')
            if result.stderr:
                raise Exception(f"{compiler[0]} runtime: {result.stderr}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"{compiler[0]} compile: {e.stderr}")
    
    def _exec_go(self, code):
        go_file = self.temp_manager.create_temp_file(code, '.go')
        result = self._run_with_timeout(['go', 'run', go_file], timeout=60)
        print(result.stdout, end='')
        if result.stderr:
            raise Exception(f"Go: {result.stderr}")
    
    def _exec_js(self, code):
        cmd = ['node', '-e', code] if not self.is_mobile else ['nodejs', '-e', code]
        result = self._run_with_timeout(cmd)
        print(result.stdout, end='')
        if result.stderr:
            raise Exception(f"JS: {result.stderr}")
    
    def _exec_lua(self, code):
        result = self._run_with_timeout(['lua', '-e', code])
        print(result.stdout, end='')
        if result.stderr:
            raise Exception(f"Lua: {result.stderr}")
    
    def _exec_ruby(self, code):
        result = self._run_with_timeout(['ruby', '-e', code])
        print(result.stdout, end='')
        if result.stderr:
            raise Exception(f"Ruby: {result.stderr}")
    
    def _exec_php(self, code):
        result = self._run_with_timeout(['php', '-r', code])
        print(result.stdout, end='')
        if result.stderr:
            raise Exception(f"PHP: {result.stderr}")
    
    def _exec_java(self, code):
        java_file = self.temp_manager.create_temp_file(code, '.java')
        class_dir = self.temp_manager.temp_dir
        
        compile_result = self._run_with_timeout(['javac', '-d', class_dir, java_file])
        if compile_result.returncode != 0:
            raise Exception(f"Java compile: {compile_result.stderr}")
        
        result = self._run_with_timeout(['java', '-cp', class_dir, 'Main'])
        print(result.stdout, end='')
        if result.stderr:
            raise Exception(f"Java runtime: {result.stderr}")
    
    def execute(self, command, line_num=0):
        try:
            command = command.strip()
            if not command or command.startswith('//'):
                return
            
            if ':=' in command:
                parts = command.split(':=', 1)
                if len(parts) == 2:
                    key, value = parts[0].strip(), parts[1].strip()
                    self._set_variable(key, value)
                return
            
            block_match = re.match(r'#(\w+)\s*\[\[(.*?)\]\]', command, re.DOTALL)
            if block_match:
                lang = block_match.group(1).lower()
                code = block_match.group(2).strip()
                
                if lang not in self.executors:
                    raise ValueError(f"Unsupported language: {lang}")
                
                code = XfawaSecurity.safe_variable_replacement(code, self.variables)
                executor, _ = self.executors[lang]
                executor(code)
                return
            
            print(command)
            
        except Exception as e:
            error_msg = f"Line {line_num}: {str(e)}" if line_num > 0 else str(e)
            print(f"Error: {error_msg}")
    
    def _set_variable(self, key, value):
        if value.isdigit():
            self.variables[key] = int(value)
        elif value.replace('.', '').isdigit():
            self.variables[key] = float(value)
        elif value.lower() in ('true', 'false'):
            self.variables[key] = value.lower() == 'true'
        elif (value.startswith('"') and value.endswith('"')) or \
             (value.startswith("'") and value.endswith("'")):
            self.variables[key] = value[1:-1]
        else:
            self.variables[key] = value
    
    def cleanup(self):
        self.temp_manager.cleanup()

class XfawaShell:
    def __init__(self, safe_mode=True, timeout=30):
        self.engine = XfawaEngine(safe_mode=safe_mode, timeout=timeout)
        self.prompt = "xfawa> "
    
    def repl(self):
        print(f"Xfawa Engine (Safe mode: {self.engine.safe_mode})")
        print("Type 'exit' to quit")
        
        while True:
            try:
                cmd = input(self.prompt).strip()
                if cmd == 'exit':
                    break
                elif cmd == 'safe off':
                    self.engine.safe_mode = False
                    print("Safe mode disabled")
                    continue
                elif cmd == 'safe on':
                    self.engine.safe_mode = True
                    print("Safe mode enabled")
                    continue
                
                self.engine.execute(cmd)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting")
                break
    
    def run_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"Running: {filename}")
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('//'):
                    print(f"[{i}/{len(lines)}] {line[:50]}..." if len(line) > 50 else f"[{i}/{len(lines)}] {line}")
                    self.engine.execute(line, i)
                    print("-" * 40)
            
            print("Execution completed")
            
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"Runtime error: {str(e)}")
    
    def cleanup(self):
        self.engine.cleanup()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Xfawa Engine')
    parser.add_argument('file', nargs='?', help='.xf file to execute')
    parser.add_argument('--safe', action='store_true', default=True, help='Enable safe mode')
    parser.add_argument('--no-safe', action='store_true', help='Disable safe mode')
    parser.add_argument('--timeout', type=int, default=30, help='Execution timeout')
    
    args = parser.parse_args()
    safe_mode = not args.no_safe
    
    shell = XfawaShell(safe_mode=safe_mode, timeout=args.timeout)
    
    try:
        if args.file:
            shell.run_file(args.file)
        else:
            shell.repl()
    finally:
        shell.cleanup()

if __name__ == '__main__':
    main()
