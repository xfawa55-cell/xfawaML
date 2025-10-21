# xfawaML Programming Language

xfawaPL is a multi-language programming language that allows embedding and mixing code from different programming languages in a single source file.

## Features

- **Multi-language support**: Mix Python, C, C++, Java, Go, JavaScript, Lua, Ruby, PHP and Shell in one file
- **Flexible execution control**: Define execution order with `xfawa.run()` in Main block
- **Cross-platform**: Compile to Linux, Windows and Android executables
- **Dependency management**: Declare dependencies in metadata block

## Installation

bash
pip install -r requirements.txt
python setup.py install

## Usage

### Compile a .xfml file

bash
xfawac examples/hello_world.xfml -o hello_world -p linux

### Run the application

For Linux
bash
tar -xzf dist/hello_world.tar.gz
cd hello_world
./hello_world

For Windows
bash
unzip dist/hello_world.zip
cd hello_world
hello_world.exe

For Android
bash
adb install dist/hello_world.apk

## Syntax

### Language Blocks

LanguageName [[
// Code in the target language
]]

### Main Block (Optional)

Main [[
// Control execution flow
xfawa.run("Language1")
xfawa.run("Language2")
]]

### Metadata Block

data [[
{
"Define_Output": true, // Enable Main block control
"dependencies": {
"python": ["numpy", "pandas"]
}
}
]]

## Examples

See the `examples/` directory for sample programs.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## License

MIT License - see [LICENSE](LICENSE) for details.