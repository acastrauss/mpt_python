from models.node_key import NodeKey, TearedKey
import models.node_enums as node_enums
from models.base_node import BaseNode 

class BranchNode(BaseNode):
    possibleBranchIndxs = "0123456789abcdef"

    def __init__(self, children, parent, value: node_enums.NodeValue) -> None:
        ''' Children shoud be of dict type, where key is str of len 1, and value is concrete Node class'''
        super().__init__(node_enums.NodeType.BRANCH, parent)
        self.Children = children
        self.Value = value

    def IsKeyInBranch(self, key: NodeKey):
        return key.Key[0] in self.Children.keys()
    
    def TearApartGivenKeyWithMine(self, key: NodeKey):
        if self.IsKeyInBranch(key):
            return TearedKey(key.Key[0], key.Key[1:])
        else:
            return TearedKey("", key.Key)

    def GetLastSimilarCharWithMyKey(self, key: NodeKey):
        if self.IsKeyInBranch(key):
            return NodeKey(key.Key[0])
        else:
            return None

    def GetBranchIndxForParticularNode(self, node:BaseNode)-> str:
        for k, v in self.Children.items():
            if id(v) == id(node):
                return k
        
        # return ''
        raise "node not in branch"