# encoding: UTF-8

import importlib
import unittest
import sys
import os


def scan_tests(module):
    for key in dir(module):
        value = getattr(module, key)
        if type(value) is type and issubclass(value, unittest.TestCase):
            yield value


def scan_solutions():
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from leetcode.path import Path
    solutions = Path(__file__).abspath.dirname.dirname / 'solutions'
    for py in [solutions.join(s) for s in os.listdir(str(solutions))]:
        if py.isfile and not py.basename.startswith('__'):
            module_name = f'solutions.{py.basename.splitext[0]}'
            yield importlib.import_module(module_name)


def for_each_case(handle):
    for module in scan_solutions():
        for case in scan_tests(module):
            handle(case)


class Run:
    def __init__(self):
        self.runner = unittest.TextTestRunner()
        self.success = True

    def __call__(self, cls: str):
        show_name = 'LeetCode::{}'.format(cls.__name__)
        print('Testing: {}'.format(show_name), file=sys.stderr)
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(cls)
        result = self.runner.run(suite)
        self.success &= result.wasSuccessful()

    def return_code(self) -> int:
        return 0 if self.success else -1


if __name__ == '__main__':
    run = Run()
    for_each_case(run)
    exit(run.return_code())
