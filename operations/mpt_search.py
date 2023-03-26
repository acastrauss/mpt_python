
from models.base_node import BaseNode
from models.node_enums import NodeType, NodeValue
from models.node_key import NodeKey

class MPTSearch:
    def __init__(self, mpt) -> None:
        self.MPT = mpt
    
    def Search(self, key: NodeKey) -> NodeValue:
        return self.__SearchInNode__(self.MPT.Root, key)

    def __SearchInNode__(self, node: BaseNode, key: NodeKey) -> NodeValue:
        if node.Type == NodeType.BRANCH:
            if node.IsKeyInBranch(key):
                return self.__SearchInNode__(node.Children[key.Key[0]], NodeKey(key.Key[1:]))
            else:
                return None
        elif node.Type == NodeType.EXTENSION:
            if key.Key.startswith(node.Key.Key):
                tearedKey = node.Key.TearApartGivenKeyWithMe(key)
                return self.__SearchInNode__(node.BranchChild, NodeKey(tearedKey.PartThatLeft))
            else:
                return None
        else: # Leaf
            if node.Key == key: 
                return node.Value
            else:
                return None