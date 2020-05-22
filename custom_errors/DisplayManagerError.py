class DisplayManagerError(Exception):
    def __init__(self, message, errors=None):
        self.message = message
        super().__init__(message, errors)

