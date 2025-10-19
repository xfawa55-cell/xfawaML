from setuptools import setup, find_packages

setup(
    name='xfawapl',
    version='1.0.0',
    description='xfawaPL Programming Language Compiler and Runtime',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyinstaller>=5.13.0',
        'docker>=6.1.3',
        'buildozer>=1.5.0',
        'kivy>=2.2.1',
        'flask>=3.0.0'
    ],
    entry_points={
        'console_scripts': [
            'xfawac = compiler.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
