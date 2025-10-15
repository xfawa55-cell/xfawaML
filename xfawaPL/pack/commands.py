from .packer import XfawaPacker

class BuildCommands:
    @staticmethod
    def execute(command):
        if command == 'zip':
            result = XfawaPacker.create_zip()
            return f"Created: {result}"
        elif command == 'standalone':
            result = XfawaPacker.create_standalone()
            return f"Created: {result}"
        else:
            return "Usage: build zip|standalone"
