# encoding: UTF-8

import enum
import itertools
import leetcode.test


class Difficulty(enum.Enum):
    Easy, Medium, Hard = 'Easy', 'Medium', 'Hard'


class Tags(enum.Enum):
    Array, LinkedList, Stack, Heep = itertools.repeat(enum.auto, times=4)
    Queue, String, Map, HashTable = itertools.repeat(enum.auto, times=4)
    Trees, BinaryTree, BinarySearchTree, Trie = itertools.repeat(enum.auto, times=4)
    Graph, DFS, BFS, TopRecursion = itertools.repeat(enum.auto, times=4)
    Pointers, TologicalSort, DivideAndConquer, DynamicProgramming = itertools.repeat(enum.auto, times=4)
    Backtracking, ReservoirSampling, Greedy, Memorization = itertools.repeat(enum.auto, times=4)
    Design, BinarySearch, Sort, BitManipulation = itertools.repeat(enum.auto, times=4)
    Minimax, Implement, Geometry, Math, Misc = itertools.repeat(enum.auto, times=5)


class Problem:
    def __init__(self, pid: int, name: str, difficulty: Difficulty, *tags: [Tags]):
        self.pid, self.name, self.difficulty, self.tags = pid, name, difficulty, tags

    def __call__(self, solution_class: type) -> type:
        # 绑定问题属性
        solution_class.problem = self
        # 绑定测试转译器
        solution_class.test = leetcode.test.TestEmitter(solution_class)
        # 转移问题属性
        for attr in dir(self):
            if not attr.startswith('_'):
                setattr(solution_class, attr, getattr(self, attr))
        return solution_class
