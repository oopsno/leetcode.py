# encoding: UTF-8

from leetcode import *
from typing import Generator


@Problem(2, 'Add Two Numbers', Difficulty.Medium, Tags.LinkedList, Tags.Math)
class Solution:
    @staticmethod
    def iterate(xs: ListNode, ys: ListNode) -> Generator[int, None, None]:
        """
        模拟十进制加法, 从低到高逐位返回各个数位
        """
        carry, val = 0, 0
        while xs is not None and ys is not None:
            carry, val = divmod(xs.val + ys.val + carry, 10)
            xs, ys = xs.next, ys.next
            yield val
        while xs is not None:
            carry, val = divmod(xs.val + carry, 10)
            xs = xs.next
            yield val
        while ys is not None:
            carry, val = divmod(ys.val + carry, 10)
            ys = ys.next
            yield val
        if carry != 0:
            yield carry

    def addTwoNumbers(self, lhs: ListNode, rhs: ListNode) -> ListNode:
        """
        从十进制加法生成的数位中构建新的链表
        """
        it = self.iterate(lhs, rhs)
        result = ListNode(next(it))
        cursor = result
        for digit in it:
            cursor.next = ListNode(digit)
            cursor = cursor.next
        return result


@Solution.test.addTwoNumbers
def examples(fn):
    require(fn(ListNode.from_list([2, 4, 3]), ListNode.from_list([5, 6, 4])) == ListNode.from_list([7, 0, 8]))
