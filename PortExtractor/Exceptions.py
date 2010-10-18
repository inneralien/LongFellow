class BaseError(Exception):
    def __init__(self, method_name, short_message, long_message):
        Exception.__init__(self)
        self.method_name = method_name
        self.error_message = error_message
        self.long_message = long_message

class FirstDetailedError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

class SecondDetailedError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)
