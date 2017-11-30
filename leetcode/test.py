#  encoding: UTF-8

"""
参考 Catch++ 设计的单元测试 DSL
"""

import inspect
import functools
import io
import abc
import unittest


class CodeGen(abc.ABC):
    @staticmethod
    def indent(level, expr):
        return '  ' * level + expr

    @abc.abstractmethod
    def codegen(self, indent_level=0) -> str:
        pass


class Equal(CodeGen):
    def __init__(self, lhs: CodeGen, rhs: CodeGen):
        self.lhs, self.rhs = lhs, rhs
        self.type = bool

    def codegen(self, indent_level=0) -> str:
        expr = f'self.assertEqual({self.lhs.codegen()}, {self.rhs.codegen()})'
        return self.indent(indent_level, expr)


class Repr(CodeGen):
    def __init__(self, value):
        self.value = value

    def codegen(self, indent_level=0) -> str:
        return repr(self.value)


class FunctionCall(CodeGen):
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        self.proxy = None

    def __eq__(self, other):
        if isinstance(other, CodeGen):
            return Equal(self, other)
        else:
            return Equal(self, Repr(other))

    def codegen(self, indent_level=0) -> str:
        args = ', '.join(map(repr, self.args))
        kwargs = ', '.join('{}={!r}'.format(key, value) for key, value in self.kwargs.items())
        if kwargs:
            return f'self.solution.{self.proxy.name}({args}, {kwargs})'
        else:
            return f'self.solution.{self.proxy.name}({args})'


class FunctionProxy:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        fc = FunctionCall(*args, **kwargs)
        fc.proxy = self
        return fc


def require(assertion: CodeGen):
    # 在调用栈上搜索断言的插入地点
    outer_frames = inspect.getouterframes(inspect.currentframe())
    for fi in outer_frames:
        endpoint = getattr(fi, 'function', None)
        if endpoint is not None and endpoint.endswith('translator'):
            fi.frame.f_locals['assertions'].append(assertion)


def translator(function_name: str, fn: callable):
    # 搜集断言
    assertions = []
    fn(FunctionProxy(name=function_name))
    #  生成代码
    ss = io.StringIO()
    ss.write(f'class {function_name.capitalize()}{fn.__name__.capitalize()}(unittest.TestCase):\n')
    ss.write(f'  def setUp(self):\n')
    ss.write(f'    self.solution = Solution()\n\n')
    ss.write(f'  def test_{fn.__name__}(self):\n')
    for a in assertions:
        print(a.codegen(indent_level=2), file=ss)
    code = ss.getvalue()
    # 在调用栈上搜索注入位置
    local = None
    for fi in inspect.getouterframes(inspect.currentframe()):
        if fi.filename == inspect.getfile(fn):
            local = fi.frame.f_locals
    # 编译并注入原始位置
    test_class = compile(code, inspect.getsource(fn), mode='exec')
    exec(test_class, local, local)


class TestEmitter:
    def __init__(self, solution_class):
        self.solution_class = solution_class

    def __getattr__(self, function_name: str) -> callable:
        return functools.partial(translator, function_name)
