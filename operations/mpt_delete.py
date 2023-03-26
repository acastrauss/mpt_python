from models.base_node import BaseNode
from models.node_enums import NodeType
from models.node_key import NodeKey


class MPTDelete:
    def __init__(self) -> None:
        self.MPT = None

    def Delete(self, key: NodeKey, mpt):
        self.MPT = mpt
        return self.__DeleteNode__(self.MPT.root, key)

    def __DeleteNode__(self, node: BaseNode, key: NodeKey):
        if node.Type == node_enums.NodeType.BRANCH:
            if node.IsKeyInBranch(key):
                self.LastBranchKeyAccessed = key.Key[0]
                return self.__DeleteNode__(node.Children[key.Key[0]], node_key.NodeKey(key.Key[1:]))
            else:
                return False
        elif node.Type == node_enums.NodeType.EXTENSION:
            if key.Key.startswith(node.Key.Key):
                tearedKey = node.Key.TearApartGivenKeyWithMe(key)
                return self.__DeleteNode__(node.BranchChild, node_key.NodeKey(tearedKey.PartThatLeft))
            else:
                return False
        else: # Leaf
            if node.Parent.Type == node_enums.NodeType.BRANCH:
                return self.__DeleteChildOfBranch__(node, key)
            else:
                raise "Leaf should have branch as parent"

    def __DeleteChildOfBranch__(self, child: BaseNode, key: NodeKey):
        pass

    def __DeleteGrandparentIsExtension__(self, child: BaseNode, key: NodeKey):
        pass

    def __DeleteGrandparentIsBranch__(self, child: BaseNode, key: NodeKey):
        pass

    def __FindSibling__(self, child: BaseNode, branchIndx: str):
        pass