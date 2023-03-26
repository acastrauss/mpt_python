from models.node_key import NodeKey
from models.node_enums import NodeValue

NOF_NODES = 2000
MIN_NODE_VALUE = -10000
MAX_NODE_VALUE = 10000
NOF_RANDOM_KEY_CHECKS = 5

class InsertValue:
    def __init__(self, key: NodeKey, value: NodeValue) -> None:
        self.Key = key
        self.Value = value