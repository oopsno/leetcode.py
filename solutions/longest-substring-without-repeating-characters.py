# encoding: UTF-8

from leetcode import *
from typing import Generator, Tuple


@Problem(3, 'Longest Substring Without Repeating Characters', Difficulty.Medium, Tags.HashTable, Tags.String, Tags.TwoPointers)
class Solution:
    @staticmethod
    def iterate(s: str) -> Generator[Tuple[int, int], None, None]:
        """
        搜索所有不包含重复字符的子串 [begin, end)
        """
        begin, sub = 0, {}
        for end, char in enumerate(s):
            if begin <= sub.get(char, -1):
                yield begin, end
                begin = sub[char] + 1
            sub[char] = end
        yield begin, len(s)

    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        检查并返回 s 中不包含重复字符的最长子串的长度
        """
        return max(r - l for l, r in self.iterate(s))


@Solution.test.lengthOfLongestSubstring
def example(fn):
    require(fn('abcabcbb') == len('abc'))
    require(fn('bbbbb') == len('b'))
    require(fn('pwwkew') == len('wke'))


@Solution.test.lengthOfLongestSubstring
def coverage(fn):
    require(fn('') == 0)
    require(fn('a') == 1)
    require(fn('aa') == 1)
    require(fn('ab') == 2)
    require(fn('abba') == len('ab'))


@Solution.test.lengthOfLongestSubstring
def profile(fn):
    require(fn('abc' * 30000) == len('abc'))
