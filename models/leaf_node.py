import models.node_enums as node_enums
import models.node_key as node_key
from models.base_node import BaseNode

class LeafNode(BaseNode):
    def __init__(self, prefix: node_enums.NodePrefix, keyEnd: node_key.NodeKey, value: node_enums.NodeValue, parent) -> None:
        super().__init__(node_enums.NodeType.LEAF, parent)
        self.Prefix = prefix
        self.Key = keyEnd
        self.Value = value

    def TearApartGivenKeyWithMine(self, key: node_key.NodeKey):
        return self.Key.TearApartGivenKeyWithMe(key)

    def GetLastSimilarCharWithMyKey(self, key: node_key.NodeKey):
        return self.Key.GetLastSimilarCharWithGivenKey(key)