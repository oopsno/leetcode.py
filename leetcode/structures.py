# encoding: UTF-8

import enum


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


class TreeBuildState(enum.Enum):
    Left, Right = 'Left', 'Right'


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    @staticmethod
    def from_list(xs):
        ts, root = [], None
        try:
            for val in xs:
                if not ts:
                    root = TreeNode(val)
                    ts.append((root, TreeBuildState.Right))
                    ts.append((root, TreeBuildState.Left))
                else:
                    node, tbs = ts.pop()
                    if val is not None:
                        if tbs is TreeBuildState.Left:
                            node.left = TreeNode(val)
                            ts.append((node, TreeBuildState.Right))
                            ts.append((node.left, TreeBuildState.Right))
                            ts.append((node.left, TreeBuildState.Left))
                        else:
                            node.right = TreeNode(val)
                            ts.append((node.right, TreeBuildState.Right))
                            ts.append((node.right, TreeBuildState.Left))

            return root
        except:
            raise ValueError('Illegal tree {!r}'.format(xs))

    def to_list(self, out=None, index=1) -> [int]:
        if out is None:
            out = []
        out.append(self.val)
        if not self.is_leaf:
            if self.left is not None:
                self.left.to_list(out=out, index=index * 2)
            else:
                out.append(None)
            if self.right is not None:
                self.right.to_list(out=out, index=index * 2 + 1)
            else:
                out.append(None)
        if index == 1:
            while out[-1] is None:
                out.pop()
        return out

    def __eq__(self, other):
        return isinstance(other, TreeNode) and self.to_list() == other.to_list()

    def __repr__(self):
        return 'TreeNode.from_list({!r})'.format(self.to_list())

    def __str__(self):
        return repr(self.to_list())
