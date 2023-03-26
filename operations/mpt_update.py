
from models.base_node import BaseNode
from models.node_enums import NodeType, NodeValue
from models.node_key import NodeKey


class MPTUpdate:
    def __init__(self, mpt) -> None:
        self.MPT = mpt

    def Update(self, key: NodeKey, value: NodeValue):
        return self.__UpdateNode__(self.MPT.Root, key, value)

    def __UpdateNode__(self, node: BaseNode, key: NodeKey, value: NodeValue):
        if node.Type == NodeType.BRANCH:
            if node.IsKeyInBranch(key):
                return self.__UpdateNode__(node.Children[key.Key[0]], NodeKey(key.Key[1:]), value)
            else:
                return None
        elif node.Type == NodeType.EXTENSION:
            if key.Key.startswith(node.Key.Key):
                tearedKey = node.Key.TearApartGivenKeyWithMe(key)
                return self.__UpdateNode__(node.BranchChild, NodeKey(tearedKey.PartThatLeft), value)
            else:
                return None
        else: # Leaf
            node.Value = value
            return node