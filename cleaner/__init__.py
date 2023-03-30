import sys
from os.path import abspath, join
from threading import Thread


def threading(func) -> ...:
    """Coloque a função decorada em uma thread."""
    def coro(*args, **kwargs) -> Thread:
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return coro


def resource_path(relative_path: str) -> str:
    """Retorna o local onde o código está rodando."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = abspath(".")

    return join(base_path, relative_path)
