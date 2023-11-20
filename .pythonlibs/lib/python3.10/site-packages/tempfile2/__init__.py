import os
import tempfile


def TemporaryFile(*args, **kwargs):
    return tempfile.TemporaryFile(*args, **kwargs)

class NamedTemporaryFileWrapper(object):
    def __init__(self, underlying, close, delete):
        self.__underlying = underlying
        self.__close = close
        self.__delete = delete

    def __enter__(self):
        result = self.__underlying.__enter__()
        if self.__close:
            self.__underlying.close()
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = self.__underlying.__exit__(exc_type, exc_val, exc_tb)
        if self.__delete:
            os.unlink(self.__underlying.name)
        return result

def NamedTemporaryFile(close=False, delete=True, *args, **kwargs):
    if delete and not close:
        return tempfile.NamedTemporaryFile(*args, delete=delete, **kwargs)
    else:
        temp_file = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
        return NamedTemporaryFileWrapper(temp_file, close=close, delete=delete)

def SpooledTemporaryFile(*args, **kwargs):
    return tempfile.SpooledTemporaryFile(*args, **kwargs)

def TemporaryDirectory(*args, **kwargs):
    return tempfile.TemporaryDirectory(*args, **kwargs)
