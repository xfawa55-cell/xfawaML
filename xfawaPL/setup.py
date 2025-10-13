from setuptools import setup

setup(
    name="xfawa",
    version="1.0.0",
    description="Languages that can be nested and run in other major languages!!",
    author="xfawa543",
    url="https://github.com/your-username/xfawa",
    py_modules=["xfawa"],
    entry_points={'console_scripts': ['xfawa=xfawa:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)