from enum import Enum

class NodeType(Enum):
    EXTENSION = 0
    LEAF = 1
    BRANCH = 2

class NodePrefix(Enum):
    EXTENSION_EVEN = 0
    EXTENSION_ODD = 1
    LEAF_EVEN = 2
    LEAF_ODD = 3
    NO_PREFIX = 4

class NodeValue:
    def __init__(self, value) -> None:
        self.Value = value
