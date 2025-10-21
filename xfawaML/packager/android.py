import os
import shutil
import subprocess
from .common import BasePackager
from compiler.error_handler import XfawaError

class AndroidPackager(BasePackager):
    def create_launch_script(self, app_dir, output_name):
        # Android使用不同的启动方式
        pass
    
    def create_archive(self, app_dir, output_name):
        # Android不需要创建压缩包
        return None
    
    def create_apk(self, app_dir, output_name):
        """使用Buildozer创建APK"""
        try:
            # 创建buildozer.spec文件
            spec_content = f"""
[app]

# (str) Title of your application
title = {output_name}

# (str) Package name
package.name = com.xfawa.{output_name}

# (str) Package domain (needed for android/ios packaging)
package.domain = org.xfawa

# (str) Source code where the main.py live
source.dir = {app_dir}

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,xf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
#android.api = 19

# (int) Minimum API required
#android.minapi = 9

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) List of directories where to find the source files for .java files.
#android.add_java_src =

# (list) List of Java files to add to the android project (only for Cython/C++ files)
#android.add_java_files =

# (list) List of patterns that will be excluded from the compilation of .py
# files into .pyo files. For example, if you have a file named 'mylib.py' that
# you want to include as source in the package, you would list it as:
# ['mylib.py']
#android.include_py = []

# (list) List of Python files to be removed from the .apk!
#android.remove_py = []

# (str) python-for-android branch to use, defaults to stable
#p4a.branch = stable

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in AndroidManifest.xml
#android.manifest.intent_filters =

# (list) Android additionnal libraries to copy into the libs folder
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Android logcat functions
#android.logcat = False

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"
#ios.codesign.release = %(ios.codesign.debug)s

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#
"""

            spec_path = os.path.join(app_dir, 'buildozer.spec')
            with open(spec_path, 'w') as f:
                f.write(spec_content)
            
            # 运行Buildozer
            subprocess.run(['buildozer', 'android', 'debug'], cwd=app_dir, check=True)
            
            # 查找生成的APK
            bin_dir = os.path.join(app_dir, 'bin')
            for file in os.listdir(bin_dir):
                if file.endswith('.apk'):
                    apk_path = os.path.join(bin_dir, file)
                    apk_dst = os.path.join('dist', f"{output_name}.apk")
                    shutil.move(apk_path, apk_dst)
                    return apk_dst
            
            raise XfawaError("APK file not found after build")
        except Exception as e:
            raise XfawaError(f"Failed to create Android APK: {str(e)}")
    
    def package(self, build_data, output_name):
        app_dir = os.path.join('dist', output_name)
        os.makedirs(app_dir, exist_ok=True)
        
        # 复制运行时文件
        self.copy_runtime_files(app_dir)
        
        # 复制构建文件
        shutil.copytree(build_data['build_dir'], os.path.join(app_dir, 'build'))
        
        # 创建APK
        apk_path = self.create_apk(app_dir, output_name)
        return apk_path
