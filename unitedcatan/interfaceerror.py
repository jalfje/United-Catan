import inspect

class InterfaceError(NotImplementedError):

    def __init__(self, my_caller):
        # www.stackoverflow.com/a/17366561
        # https://docs.python.org/3/library/inspect.html
        caller_class = my_caller.__class__.__name__
        caller_function = inspect.currentframe().f_back.f_code.co_name
        error_str = "class {0} doesn't implement {1}".format(caller_class, caller_function)
        super(InterfaceError, self).__init__(error_str)

