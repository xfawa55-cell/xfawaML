#!/usr/bin/env python3
import argparse
import sys
from compiler.parser import XfawaParser
from compiler.code_generator import CodeGenerator
from compiler.dependency_resolver import DependencyResolver
from compiler.error_handler import XfawaError
from packager.linux import LinuxPackager
from packager.windows import WindowsPackager
from packager.android import AndroidPackager

def main():
    parser = argparse.ArgumentParser(description='xfawaML Compiler')
    parser.add_argument('source', help='Source file (.xfml)')
    parser.add_argument('-o', '--output', default='app', help='Output name')
    parser.add_argument('-p', '--platform', choices=['linux', 'windows', 'android'], 
                        default='linux', help='Target platform')
    args = parser.parse_args()
    
    if not args.source.endswith('.xfml'):
        print("Error: Source file must have .xfml extension")
        sys.exit(1)
    
    try:
        # 读取源代码
        with open(args.source, 'r') as f:
            source_code = f.read()
        
        # 解析源代码
        parser = XfawaParser(source_code, args.source)
        parsed_data = parser.parse()
        
        # 解析依赖
        resolver = DependencyResolver()
        if 'dependencies' in parsed_data['data']:
            resolved_deps = resolver.resolve(parsed_data['data']['dependencies'])
            parsed_data['data']['dependencies'] = resolved_deps
        
        # 生成代码
        generator = CodeGenerator()
        build_data = generator.generate(parsed_data, args.output)
        
        # 打包应用
        if args.platform == 'linux':
            packager = LinuxPackager()
        elif args.platform == 'windows':
            packager = WindowsPackager()
        elif args.platform == 'android':
            packager = AndroidPackager()
        
        output_path = packager.package(build_data, args.output)
        
        print(f"Successfully built: {output_path}")
        
    except XfawaError as e:
        print(f"Compilation error: {e.message}")
        if e.file_path:
            print(f"File: {e.file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
