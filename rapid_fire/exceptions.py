

class BaseError(Exception):
    """
    Baseclass for all kunai errors.
    """
    pass


class TerminateLoop(BaseError):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ParseError(BaseError):
    """
    """
