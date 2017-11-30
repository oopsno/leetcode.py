# encoding: UTF-8

from leetcode import *


@Problem(94, 'Binary Tree Inorder Traversal', Difficulty.Medium, Tags.HashTable, Tags.Stack, Tags.Trees)
class Solution:
    def travel(self, root: TreeNode, out: [int]):
        if root is None:
            return out
        else:
            self.travel(root.left, out)
            out.append(root.val)
            self.travel(root.right, out)

    def inorderTraversal(self, root: TreeNode) -> [int]:
        out = []
        self.travel(root, out)
        return out

@Solution.test.inorderTraversal
def examples(fn):
    require(fn(None) == [])
    require(fn(TreeNode.from_list([1, None, 2, 3])) == [1, 3, 2])
