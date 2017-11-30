# encoding: UTF-8


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    @staticmethod
    def from_list(xs):
        if len(xs) is 0:
            return None
        it = iter(xs)
        xs = ListNode(next(it))
        cursor = xs
        for val in it:
            cursor.next = ListNode(val)
            cursor = cursor.next
        return xs

    def to_list(self):
        xs, cursor = [], self
        while cursor is not None:
            xs.append(cursor.val)
            cursor = cursor.next
        return xs

    def __eq__(self, other):
        return isinstance(other, ListNode) and self.to_list() == other.to_list()

    def __repr__(self):
        return 'ListNode.from_list({!r})'.format(self.to_list())

    def __str__(self):
        return '({})'.format(' -> '.join(self.to_list()))
