# encoding: UTF-8

"""
懒人的 Path
"""


class Path:
    """
    懒人的文件路径工具
    NOTE: 熟读并背诵 os.path
    """

    def __init__(self, path):
        self.path = path

    def __get__(self, instance, owner) -> str:
        return self.path

    def __getitem__(self, item):
        return self.slash(item)

    def __truediv__(self, other: str):
        if isinstance(other, str) or type(other) is type(self):
            return self.slash(str(other))
        else:
            raise NotImplemented

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return self.path == str(other)

    def __getattr__(self, item):
        """
        熟读并背诵
        + os.path
        + str
        """
        import os
        import inspect
        import functools
        fn = getattr(os.path, item, None)
        if fn is None:
            fn = getattr(self.path, item, None)
            if fn is None or not callable(fn):
                raise AttributeError('{!r} object has no attribute {!r}'.format(self.__class__.__name__, item))
            else:
                return fn
        if callable(fn):
            if len(inspect.signature(fn).parameters) is 1:
                rtv = fn(self.path)
                if isinstance(rtv, str):
                    return Path(rtv)
                else:
                    return rtv
            else:
                @functools.wraps(fn)
                def __partial__(*args, **kwargs):
                    return Path(fn(self.path, *args, **kwargs))

                return __partial__
        else:
            return fn

    def open(self, mode: str):
        return open(self.path, mode)

    def slash(self, component: str):
        if not isinstance(component, str):
            raise TypeError('path component must be str, got {!r}'.format(type(component)))
        path = self.join(component)
        if path.exists:
            return path
        else:
            raise FileNotFoundError('{!r} not exists'.format(path))
