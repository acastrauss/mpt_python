from models.node_enums import NodeType

class BaseNode:
    def __init__(self, nodeType: NodeType, parent) -> None:
        self.Type = nodeType
        self.Parent = parent
