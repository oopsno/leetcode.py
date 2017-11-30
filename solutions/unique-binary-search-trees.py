# encoding: UTF-8

from leetcode import *
from functools import reduce
from operator import add

# 似乎 LeetCode 针对每个测试用例创建全新的 Solution 对象, 因此使用全局缓存
UBST = [1, 1]

@Problem(96, 'Unique Binary Search Trees', Difficulty.Medium, Tags.DynamicProgramming, Tags.Trees)
class Solution:
    def numTrees(self, n: int) -> int:
        for total in range(len(UBST), n + 1):
            UBST.append(reduce(add, (UBST[p] * UBST[total - p - 1] for p in range(total))))
        return UBST[n]


@Solution.test.numTrees
def examples(fn):
    require(fn(0) == 1)
    require(fn(1) == 1)
    require(fn(2) == 2)
    require(fn(3) == 5)
    require(fn(4) == 14)
