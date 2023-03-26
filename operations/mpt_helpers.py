
from models.branch_node import BranchNode
from models.leaf_node import LeafNode
from models.node_enums import NodeType
from models.node_key import NodeKey


def CreateEmptyBranchWithParent(parent):
    return BranchNode(
        children={},
        parent=parent,
        value=None
    )

def AssignLeafToBranch(newLeafFullKeyStr, leafValue, branch):
    slicedNewLeafKey = NodeKey(newLeafFullKeyStr[1:])
    branch.Children[newLeafFullKeyStr[0]] = LeafNode(
        prefix=slicedNewLeafKey.GetPrefix(NodeType.LEAF),
        keyEnd=slicedNewLeafKey,
        value=leafValue,
        parent=branch
    )