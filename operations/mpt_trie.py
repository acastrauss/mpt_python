from models.base_node import BaseNode
from models.leaf_node import LeafNode
from models.node_enums import NodeType, NodeValue
from models.node_key import NodeKey, TearedKey
from operations.mpt_delete import MPTDelete
from operations.mpt_insert import MPTInsert
from operations.mpt_search import MPTSearch
from operations.mpt_update import MPTUpdate


class MPT:
    def __init__(self, root: BaseNode) -> None:
        self.Root = root
        self.LastSimilarNode: BaseNode = None
        self.TearedKey: TearedKey = None
        self.DeleteOps = MPTDelete(self)
        self.UpdateOps = MPTUpdate(self)
        self.SearchOps = MPTSearch(self)
        self.InsertOps = MPTInsert(self, self.UpdateOps)

    def CreateMPT(key: NodeKey, value: NodeValue):
        return MPT(LeafNode(
            key.GetPrefix(NodeType.LEAF),
            key,
            value,
            None
        ))

    def Insert(self, key: NodeKey, value: NodeValue):
        self.InsertOps.Insert(key, value)

    def Search(self, key: NodeKey) -> NodeValue:
        return self.SearchOps.Search(key)

    def Update(self, key: NodeKey, value: NodeValue):
        return self.UpdateOps.Update(key, value)

    def Delete(self, key: NodeKey):
        return self.DeleteOps.Delete(key)