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

    def GetBytes(self):
        return self.Value.to_bytes(4, 'big', signed=True)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return __o.Value == self.Value
        else:
            return False

