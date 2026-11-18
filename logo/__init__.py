import os
import sys

if sys.version_info >= (3, 9):  # pragma: no cover
    from importlib.resources import files as _files

    def resolve(resource: str) -> str:
        """Resolve an ``@logo/<resource>`` reference to an absolute path."""
        name = resource[len("@logo/") :] if resource.startswith("@logo/") else resource
        return str(_files("logo").joinpath(name))

else:  # pragma: no cover

    def resolve(resource: str) -> str:
        """Resolve an ``@logo/<resource>`` reference to an absolute path."""
        name = resource[len("@logo/") :] if resource.startswith("@logo/") else resource
        return os.path.join(os.path.dirname(__file__), name)
