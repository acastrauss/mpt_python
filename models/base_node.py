from models.node_enums import NodeType

class BaseNode:
    instanceId = 0
    def __init__(self, nodeType: NodeType, parent) -> None:
        self.Type = nodeType
        self.Parent = parent
        self.InstanceId = BaseNode.instanceId
        BaseNode.instanceId += 1
