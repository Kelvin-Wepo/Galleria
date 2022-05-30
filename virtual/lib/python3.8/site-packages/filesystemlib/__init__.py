__version__ = None

try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("filesystemlib").version
except Exception:
    pass


from .chmod import chmod
from .makedirs import makedirs
from .move import move
from .walk import walk
