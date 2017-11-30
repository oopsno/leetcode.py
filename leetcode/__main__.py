# encoding: UTF-8

import inspect
import importlib
import unittest
from .path import Path
import argparse
import sys
import os
import re


class Action:
    def __init__(self, solution):
        solution = Path(solution)
        if not solution.exists:
            raise FileNotFoundError(solution)
        else:
            module_name = solution.splitext[0].replace(os.path.sep, '.')
            module = importlib.import_module(module_name)
            self.module = module
            self.solution = module.Solution
            self.tests = []
            for key in dir(module):
                val = getattr(module, key)
                if type(val) is type and issubclass(val, unittest.TestCase):
                    self.tests.append(val)


class Compile(Action):
    def run(self) -> bool:
        # 分析源文件
        filename = inspect.getfile(self.solution)
        solution_lines, begin = inspect.getsourcelines(self.solution)
        source = open(filename).readlines()
        # 原样输出 Solution 之前引入 leetcode 之外的行
        for line in map(str.strip, source[:begin - 2]):
            if not line or re.match('from leetcode import.*', line) or re.match('import leetcode.*', line):
                continue
            else:
                print(line)
        # 输出不带装饰器的 Solution
        for line in solution_lines:
            print(line, end='')


class Test(Action):
    def run(self) -> bool:
        success = True
        runner = unittest.TextTestRunner()
        for test in self.tests:
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(test)
            success &= runner.run(suite).wasSuccessful()
        return success


def parse_args():
    parser = argparse.ArgumentParser(description='LeetCode.py 命令行工具', prog='leetcode')
    parser.add_argument('action', type=str, help='动作, 可以为: compile, test')
    parser.add_argument('solution', type=str, help='solutions/*.py')
    try:
        args = parser.parse_args()
        if args.action == 'compile':
            return Compile(args.solution)
        elif args.action == 'test':
            return Test(args.solution)
        else:
            print(f'Unknown action {args.action}', file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
        parser.print_help()
        exit(-1)


if __name__ == '__main__':
    action = parse_args()
    if not action.run():
        exit(-1)
