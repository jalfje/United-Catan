import inspect


class InterfaceError(NotImplementedError):

    def __init__(self, myCaller):
        # www.stackoverflow.com/a/17366561
        # https://docs.python.org/3/library/inspect.html
        callerClass = myCaller.__class__.__name__
        callerFunction = inspect.currentframe().f_back.f_code.co_name
        errorStr = "class {0} doesn't implement {1}".format(callerClass,
                                                            callerFunction)
        super(InterfaceError, self).__init__(errorStr)


# TODO: change the parent class
class NoHexNumberError(Exception):
    pass
