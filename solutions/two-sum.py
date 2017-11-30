# encoding: UTF-8

from leetcode import *
import collections
from typing import Union

Pair = collections.namedtuple('Pair', ['position', 'value'])


@Problem(1, 'Two Sum', Difficulty.Easy, Tags.Array, Tags.HashTable)
class Solution:
    """
    Given an array of integers, return indices of the two numbers such that they add up to a specific target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.
    """

    def twoSum(self, nums: [int], target: int) -> [int]:
        """
        排序 + 二分搜索
        """
        n = len(nums)
        xs = [Pair(i, x) for i, x in enumerate(nums)]
        xs.sort(key=lambda x: x.value)
        for i, x in enumerate(xs):
            another = self.binary_search(target - x.value, xs, i + 1, n)
            if another is None:
                continue
            else:
                if x.position < another:
                    return [x.position, another]
                else:
                    return [another, x.position]

    def binary_search(self, x: int, xs: [Pair], begin: int, end: int) -> Union[int, None]:
        if not 0 <= begin < end <= len(xs):
            return None
        mid = (begin + end) // 2
        pivot = xs[mid]
        if pivot.value == x:
            return pivot.position
        elif pivot.value > x:
            return self.binary_search(x, xs, begin, mid)
        else:
            return self.binary_search(x, xs, mid + 1, end)


@Solution.test.twoSum
def examples(fn):
    require(fn([2, 7, 11, 15], 9) == [0, 1])
    require(fn([3, 2, 4], 6) == [1, 2])
