import models.node_enums as node_enums
import models.node_key as node_key
from models.base_node import BaseNode

class ExtensionNode(BaseNode):
    def __init__(self, prefix: node_enums.NodePrefix, sharedKey: node_key.NodeKey, branchChild, parent) -> None:
        super().__init__(node_enums.NodeType.EXTENSION, parent)
        self.Prefix = prefix
        self.Key = sharedKey
        self.BranchChild = branchChild

    def TearApartGivenKeyWithMine(self, key: node_key.NodeKey):
        return self.Key.TearApartGivenKeyWithMe(key)

    def GetLastSimilarCharWithMyKey(self, key: node_key.NodeKey):
        return self.Key.GetLastSimilarCharWithGivenKey(key)