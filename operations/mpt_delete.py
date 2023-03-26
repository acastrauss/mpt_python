from models.base_node import BaseNode
from models.extension_node import ExtensionNode
from models.leaf_node import LeafNode
from models.node_enums import NodeType
from models.node_key import NodeKey


class MPTDelete:
    def __init__(self, mpt) -> None:
        self.MPT = mpt

    def Delete(self, key: NodeKey):
        return self.__DeleteNode__(self.MPT.Root, key)

    def __DeleteNode__(self, node: BaseNode, key: NodeKey):
        if node.Type == NodeType.BRANCH:
            if node.IsKeyInBranch(key):
                self.MPT.LastBranchKeyAccessed = key.Key[0]
                return self.__DeleteNode__(node.Children[key.Key[0]], NodeKey(key.Key[1:]))
            else:
                return False
        elif node.Type == NodeType.EXTENSION:
            if key.Key.startswith(node.Key.Key):
                tearedKey = node.Key.TearApartGivenKeyWithMe(key)
                return self.__DeleteNode__(node.BranchChild, NodeKey(tearedKey.PartThatLeft))
            else:
                return False
        else: # Leaf
            if node.Parent.Type == NodeType.BRANCH:
                return self.__DeleteChildOfBranch__(node, key)
            else:
                raise "Leaf should have branch as parent"

    def __DeleteChildOfBranch__(self, child: BaseNode, key: NodeKey):
        nofSiblings = len(child.Parent.Children.keys())
                
        if nofSiblings == 2: 
            '''
                Only 1 leaf will be left after we delete current one,
                because of that we need to transform the branch 
            '''
            if child.Parent.Parent.Type == NodeType.BRANCH:
                self.__DeleteGrandparentIsBranch__(child, key)
            elif child.Parent.Parent.Type == NodeType.EXTENSION:
                self.__DeleteGrandparentIsExtension__(child, key)
            else:
                raise "leaf can not be a parent"
        else:
            '''
                We can safely delete just this leaf, since branch will have >=2 children left
                and is still valid branch
            '''
            del child.Parent.Children[self.MPT.LastBranchKeyAccessed]

        return True

    def __DeleteGrandparentIsExtension__(self, child: BaseNode, key: NodeKey):
        sibling = self.__FindSibling__(child, self.MPT.LastBranchKeyAccessed)
        if sibling.Type == NodeType.LEAF:
            '''
                Parent extension becomes leaf, with key: extKey + branchIndx + leafSiblingKey
            '''
            newLeafKey = NodeKey(child.Parent.Parent.Key.Key + self.MPT.LastBranchKeyAccessed + sibling.Key.Key)
            newLeaf = LeafNode(
                prefix=newLeafKey.GetPrefix(NodeType.LEAF),
                keyEnd=newLeafKey,
                value=sibling.Value,
                parent=child.Parent.Parent.Parent
            )

            if child.Parent.Parent.Parent is None:
                self.Root = newLeaf
            else: # 3rd degree parent is branch 
                grandParentBranchIndx = child.Parent.Parent.Parent.GetBranchIndxForParticularNode(child.Parent.Parent)
                child.Parent.Parent.Parent.Children[grandParentBranchIndx] = newLeaf
        elif sibling.Type == NodeType.EXTENSION:
            '''
                Merge grandparent extension, branch, and sibling extension into new extension
            '''
            newExtensionKey = NodeKey(child.Parent.Parent.Key.Key + self.MPT.LastBranchKeyAccessed + sibling.Key.Key)
            newExtension = ExtensionNode(
                prefix=newExtensionKey.GetPrefix(NodeType.EXTENSION),
                sharedKey=newExtensionKey,
                branchChild=sibling.BranchChild,
                parent=child.Parent.Parent.Parent
            )

            if child.Parent.Parent.Parent is None:
                self.Root = newExtension
            else: # 3rd degree parent is branch 
                grandParentBranchIndx = child.Parent.Parent.Parent.GetBranchIndxForParticularNode(child.Parent.Parent)
                child.Parent.Parent.Parent.Children[grandParentBranchIndx] = newExtension
        else: # sibling is branch
            '''
                Parent of child (branch) becomes and extension merged with it's parent extension
            '''
            newExtensionKey = NodeKey(child.Parent.Parent.Key.Key + self.MPT.LastBranchKeyAccessed)
            newExtension = ExtensionNode(
                prefix=newExtensionKey.GetPrefix(NodeType.EXTENSION),
                sharedKey=newExtensionKey,
                branchChild=sibling,
                parent=child.Parent.Parent
            )
            
            if child.Parent.Parent.Parent is None:
                self.Root = newExtension
            else: # 3rd degree parent is branch 
                grandParentBranchIndx = child.Parent.Parent.Parent.GetBranchIndxForParticularNode(child.Parent.Parent)
                child.Parent.Parent.Parent.Children[grandParentBranchIndx] = newExtension

    def __DeleteGrandparentIsBranch__(self, child: BaseNode, key: NodeKey):
        sibling = self.__FindSibling__(child, self.MPT.LastBranchKeyAccessed)
        if sibling.Type == NodeType.LEAF:
            '''
                Child.Parent branch becomes leaf, with key branchIndx + sibling.Key
            '''
            newLeafKey = NodeKey(self.MPT.LastBranchKeyAccessed + sibling.Key.Key)
            newLeaf = LeafNode(
                prefix=newLeafKey.GetPrefix(NodeType.LEAF),
                keyEnd=newLeafKey,
                parent=child.Parent.Parent,
                value=sibling.Value
            )

            parentBranchIndx = child.Parent.Parent.GetBranchIndxForParticularNode(child.Parent)
            child.Parent.Parent.Children[parentBranchIndx] = newLeaf

        elif sibling.Type == NodeType.EXTENSION:
            '''
                Branch get merged with sibling extension
                Sibling extension new key is: branchIndx + extensionOldKey
            '''
            newExtensionKey = NodeKey(self.MPT.LastBranchKeyAccessed + sibling.Key.Key)
            sibling.Key = newExtensionKey
            sibling.Parent = child.Parent.Parent

            parentBranchIndx = child.Parent.Parent.GetBranchIndxForParticularNode(child.Parent)
            child.Parent.Parent.Children[parentBranchIndx] = sibling
        else: # sibling is branch
            '''
                Current branch parent becomes an extension
                Not sure if this is right
            '''
            newExtensionKey = NodeKey(key.Key)
            newExtension = ExtensionNode(
                prefix=newExtensionKey.GetPrefix(NodeType.EXTENSION),
                sharedKey=newExtensionKey,
                branchChild=sibling,
                parent=child.Parent.Parent
            )

            parentBranchIndx = child.Parent.Parent.GetBranchIndxForParticularNode(child.Parent)
            child.Parent.Parent.Children[parentBranchIndx] = newExtension


    def __FindSibling__(self, child: BaseNode, branchIndx: str):
        if child.Parent.Type == NodeType.BRANCH:
            for k, v in child.Parent.Children.items():
                if k != branchIndx:
                    return v
            raise "coudln't find sibling"
        else:
            raise "parent is not a branch"