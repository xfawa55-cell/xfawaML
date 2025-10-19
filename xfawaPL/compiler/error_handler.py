class XfawaError(Exception):
    def __init__(self, message, file_path=None, line=None):
        self.message = message
        self.file_path = file_path
        self.line = line
        
    def __str__(self):
        if self.file_path:
            if self.line:
                return f"{self.file_path}:{self.line}: {self.message}"
            return f"{self.file_path}: {self.message}"
        return self.message
