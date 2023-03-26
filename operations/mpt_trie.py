from models.base_node import BaseNode
from models.branch_node import BranchNode
from models.extension_node import ExtensionNode
import models.node_enums as node_enums
import models.node_key as node_key
import models.leaf_node as leaf_node


class MPT:
    def __init__(self, root: BaseNode) -> None:
        self.Root = root
        self.LastSimilarNode: BaseNode = None
        self.TearedKey: node_key.TearedKey = None

    def CreateMPT(key: node_key.NodeKey, value: node_enums.NodeValue):
        return MPT(leaf_node.LeafNode(
            key.GetPrefix(node_enums.NodeType.LEAF),
            key,
            value,
            None
        ))

    def Insert(self, key: node_key.NodeKey, value: node_enums.NodeValue):
        self.__GetLastSimilarNode__(self.Root, key)

        if self.LastSimilarNode.Type == node_enums.NodeType.LEAF:
            '''
                Make extension from leaf, and add branch as a child with
                2 children, one with current leaf sliced key
                and other with new sliced key
                If there are no similarities between keys, create just a branch, no extension
            '''
            similiaritiesNum = self.LastSimilarNode.Key.CountSimilaritiesWithKey(node_key.NodeKey(f"{self.TearedKey.TearedPart}{self.TearedKey.PartThatLeft}"))
            if self.LastSimilarNode.Key.Key == f"{self.TearedKey.TearedPart}{self.TearedKey.PartThatLeft}":
                self.Update(key, value)
                return
            
            if similiaritiesNum > 0:
                sharedKey = self.LastSimilarNode.Key.GetSharedKeyWithGivenKey(node_key.NodeKey(f"{self.TearedKey.TearedPart}{self.TearedKey.PartThatLeft}"))

                newExtension = ExtensionNode(
                    prefix=sharedKey.GetPrefix(node_enums.NodeType.EXTENSION),
                    sharedKey=sharedKey,
                    branchChild=None,
                    parent=self.LastSimilarNode.Parent
                )

                newBranch = BranchNode(
                    children={},
                    parent=newExtension,
                    value=None
                )

                newExtension.BranchChild = newBranch

                lsnKeyLen = self.LastSimilarNode.Key.GetLen()
                newLeaf1Key = node_key.NodeKey(
                    self.LastSimilarNode.Key.Key[lsnKeyLen-len(self.TearedKey.PartThatLeft):]
                )

                fixedNewLeaf1Key = node_key.NodeKey(newLeaf1Key.Key[1:])
                newBranch.Children[newLeaf1Key.Key[0]] = leaf_node.LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(node_enums.NodeType.LEAF),
                    keyEnd=fixedNewLeaf1Key,
                    value=self.LastSimilarNode.Value,
                    parent=newBranch
                )

                newLeaf2Key = self.TearedKey.PartThatLeft
                fixedNewLeaf2Key = node_key.NodeKey(newLeaf2Key[1:])
                newBranch.Children[newLeaf2Key[0]] = leaf_node.LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(node_enums.NodeType.LEAF),
                    keyEnd=fixedNewLeaf2Key,
                    value=value,
                    parent=newBranch
                )

                if self.LastSimilarNode.Parent == None:
                    self.Root = newExtension
                elif self.LastSimilarNode.Parent.Type == node_enums.NodeType.BRANCH:
                    self.LastSimilarNode.Parent.Children[self.LastBranchKeyAccessed] = newExtension
                else:
                    raise "only branch can be a parent of a leaf"
            else: # just create a branch
                newBranch = BranchNode(
                    children={},
                    parent=self.LastSimilarNode.Parent,
                    value=None
                )

                lsnKeyLen = self.LastSimilarNode.Key.GetLen()
                newLeaf1Key = node_key.NodeKey(
                    self.LastSimilarNode.Key.Key[lsnKeyLen-len(self.TearedKey.PartThatLeft):]
                )

                fixedNewLeaf1Key = node_key.NodeKey(newLeaf1Key.Key[1:])
                newBranch.Children[newLeaf1Key.Key[0]] = leaf_node.LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(node_enums.NodeType.LEAF),
                    keyEnd=fixedNewLeaf1Key,
                    value=self.LastSimilarNode.Value,
                    parent=newBranch
                )

                newLeaf2Key = self.TearedKey.PartThatLeft
                fixedNewLeaf2Key = node_key.NodeKey(newLeaf2Key[1:])
                newBranch.Children[newLeaf2Key[0]] = leaf_node.LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(node_enums.NodeType.LEAF),
                    keyEnd=fixedNewLeaf2Key,
                    value=value,
                    parent=newBranch
                )

                if self.LastSimilarNode.Parent == None:
                    self.Root = newBranch
                elif self.LastSimilarNode.Parent.Type == node_enums.NodeType.BRANCH:
                    self.LastSimilarNode.Parent.Children[self.LastBranchKeyAccessed] = newBranch
                else:
                    raise "only branch can be a parent of a leaf"

        elif self.LastSimilarNode.Type == node_enums.NodeType.BRANCH:
            if not self.LastSimilarNode.IsKeyInBranch(node_key.NodeKey(self.TearedKey.PartThatLeft)):
                newLeafKey = node_key.NodeKey(self.TearedKey.PartThatLeft[1:])
                self.LastSimilarNode.Children[self.TearedKey.PartThatLeft[0]] = leaf_node.LeafNode(
                    prefix=newLeafKey.GetPrefix(node_enums.NodeType.LEAF),
                    keyEnd=newLeafKey,
                    parent=self.LastSimilarNode,
                    value=value
                )
            else:
                self.Update(key, value)
            
        else:
            tempKey = node_key.NodeKey(f"{self.TearedKey.TearedPart}{self.TearedKey.PartThatLeft}")
            similiaritiesNum = self.LastSimilarNode.Key.CountSimilaritiesWithKey(tempKey)
            
            if similiaritiesNum > 0: # make new extension from two keys
                newCommonKey: node_key.NodeKey = self.LastSimilarNode.Key.GetSharedKeyWithGivenKey(tempKey)

                newCommonExtension = ExtensionNode(
                    prefix=newCommonKey.GetPrefix(node_enums.NodeType.EXTENSION),
                    sharedKey=newCommonKey,
                    parent=self.LastSimilarNode.Parent,
                    branchChild=None
                )

                newBranch = BranchNode(
                    children={},
                    parent=newCommonExtension,
                    value=None
                )

                newCommonExtension.BranchChild = newBranch

                newLeafKey = newCommonKey.TearApartGivenKeyWithMe(node_key.NodeKey(self.TearedKey.PartThatLeft))
                nlkFixed = node_key.NodeKey(newLeafKey.PartThatLeft[1:])

                newBranch.Children[newLeafKey.PartThatLeft[0]] = leaf_node.LeafNode(
                    prefix=nlkFixed.GetPrefix(node_enums.NodeType.LEAF),
                    keyEnd=nlkFixed,    
                    parent=newBranch,
                    value=value
                )

                prevExtTearedKey = newCommonKey.TearApartGivenKeyWithMe(self.LastSimilarNode.Key) # 7

                if len(prevExtTearedKey.PartThatLeft) == 1:
                    newBranch.Children[prevExtTearedKey.PartThatLeft[0]] = self.LastSimilarNode.BranchChild
                else:
                    tempKey1 = node_key.NodeKey(newCommonKey.Key + prevExtTearedKey.PartThatLeft[0])
                    keyToUse1 = tempKey1.TearApartGivenKeyWithMe(prevExtTearedKey.PartThatLeft)
                    ktu = node_key.NodeKey(keyToUse1.PartThatLeft)
                    newChildExt1 = ExtensionNode(
                        prefix=ktu.GetPrefix(node_enums.NodeType.EXTENSION),
                        branchChild=self.LastSimilarNode.BranchChild,
                        parent=newBranch,
                        sharedKey=ktu
                    )
                    newBranch.Children[prevExtTearedKey.PartThatLeft[0]] = newChildExt1

                if self.LastSimilarNode.Parent == None:
                    self.Root = newCommonExtension
                elif self.LastSimilarNode.Parent.Type == node_enums.NodeType.BRANCH: 
                    self.LastSimilarNode.Parent.Children[self.LastBranchKeyAccessed] = newCommonExtension
                else:
                    raise "Extension has wrong parent"
            else: 
                ''' Extension doesn't have any similarities with new key,
                    Create new branch that will be a parent to last similar node i.e. extension, and new key
                    If extension keyLen == 1 -> extension.Child will be at branch[extensionKey]
                    Else slice extension key
                '''
                newBranch = BranchNode(
                    children={},
                    parent=self.LastSimilarNode.Parent,
                    value=None
                )

                if self.LastSimilarNode.Parent == None:
                    self.Root = newBranch
                elif self.LastSimilarNode.Parent.Type == node_enums.NodeType.BRANCH: 
                    self.LastSimilarNode.Parent.Children[self.LastBranchKeyAccessed] = newBranch
                else:
                    raise "Extension has wrong parent"

                if self.LastSimilarNode.Key.GetLen() == 1:
                    newBranch.Children[self.LastSimilarNode.Key.Key[0]] = self.LastSimilarNode.BranchChild
                    self.LastSimilarNode.BranchChild.Parent = newBranch
                else:
                    branchIndx = self.LastSimilarNode.Key.Key[0]
                    newExtKey = node_key.NodeKey(self.LastSimilarNode.Key.Key[1:])
                    newExtension = ExtensionNode(
                        prefix=newExtKey.GetPrefix(node_enums.NodeType.EXTENSION),
                        sharedKey=newExtKey,
                        branchChild=self.LastSimilarNode.BranchChild,
                        parent=newBranch
                    )
                    newBranch.Children[branchIndx] = newExtension
                    self.LastSimilarNode.BranchChild.Parent = newExtension

                newLeafKey = node_key.NodeKey(tempKey.Key[1:])
                leafBranchIndx = tempKey.Key[0]
                newLeaf = leaf_node.LeafNode(
                    prefix=newLeafKey.GetPrefix(node_enums.NodeType.LEAF),
                    keyEnd=newLeafKey,
                    value=value,
                    parent=newBranch
                )
                newBranch.Children[leafBranchIndx] = newLeaf

    def __GetLastSimilarNode__(self, nodeToCompareTo, key: node_key.NodeKey):
        tearedKey:node_key.TearedKey = nodeToCompareTo.TearApartGivenKeyWithMine(key)

        if nodeToCompareTo.Type == node_enums.NodeType.BRANCH:
            if nodeToCompareTo.IsKeyInBranch(key):
                branchIndx = key.Key[0]
                self.LastBranchKeyAccessed = branchIndx
                self.__GetLastSimilarNode__(nodeToCompareTo.Children[branchIndx], node_key.NodeKey(tearedKey.PartThatLeft))
            else:
                self.LastSimilarNode = nodeToCompareTo
                self.TearedKey = tearedKey
                
        elif nodeToCompareTo.Type == node_enums.NodeType.EXTENSION:
            if key.Key.startswith(nodeToCompareTo.Key.Key):
                self.__GetLastSimilarNode__(nodeToCompareTo.BranchChild, node_key.NodeKey(tearedKey.PartThatLeft))
            else:
                self.LastSimilarNode = nodeToCompareTo # key doesn't start with extension key
                self.TearedKey = tearedKey
        else:
            lastSimilar = nodeToCompareTo

            self.LastSimilarNode = lastSimilar
            self.TearedKey = tearedKey

    def Search(self, key: node_key.NodeKey) -> node_enums.NodeValue:
        return self.__SearchInNode__(self.Root, key)

    def __SearchInNode__(self, node: BaseNode, key: node_key.NodeKey) -> node_enums.NodeValue:
        if node.Type == node_enums.NodeType.BRANCH:
            if node.IsKeyInBranch(key):
                return self.__SearchInNode__(node.Children[key.Key[0]], node_key.NodeKey(key.Key[1:]))
            else:
                return None
        elif node.Type == node_enums.NodeType.EXTENSION:
            if key.Key.startswith(node.Key.Key):
                tearedKey = node.Key.TearApartGivenKeyWithMe(key)
                return self.__SearchInNode__(node.BranchChild, node_key.NodeKey(tearedKey.PartThatLeft))
            else:
                return None
        else: # Leaf
            if node.Key == key: 
                return node.Value
            else:
                return None

    def Update(self, key: node_key.NodeKey, value: node_enums.NodeValue):
        return self.__UpdateNode__(self.Root, key, value)

    def __UpdateNode__(self, node: BaseNode, key: node_key.NodeKey, value: node_enums.NodeValue):
        if node.Type == node_enums.NodeType.BRANCH:
            if node.IsKeyInBranch(key):
                return self.__UpdateNode__(node.Children[key.Key[0]], node_key.NodeKey(key.Key[1:]), value)
            else:
                return None
        elif node.Type == node_enums.NodeType.EXTENSION:
            if key.Key.startswith(node.Key.Key):
                tearedKey = node.Key.TearApartGivenKeyWithMe(key)
                return self.__UpdateNode__(node.BranchChild, node_key.NodeKey(tearedKey.PartThatLeft), value)
            else:
                return None
        else: # Leaf
            node.Value = value
            return node

    def Delete(self, key: node_key.NodeKey):
        return self.__DeleteNode__(self.Root, key)

    def __DeleteNode__(self, node: BaseNode, key: node_key.NodeKey):
        if node.Type == node_enums.NodeType.BRANCH:
            if node.IsKeyInBranch(key):
                self.LastBranchKeyAccessed = key.Key[0]
                return self.__DeleteNode__(node.Children[key.Key[0]], node_key.NodeKey(key.Key[1:]))
            else:
                return False
        elif node.Type == node_enums.NodeType.EXTENSION:
            if key.Key.startswith(node.Key.Key):
                tearedKey = node.Key.TearApartGivenKeyWithMe(key)
                return self.__DeleteNode__(node.BranchChild, node_key.NodeKey(tearedKey.PartThatLeft))
            else:
                return False
        else: # Leaf
            if node.Parent.Type == node_enums.NodeType.BRANCH:
                return self.__DeleteChildOfBranch__(node, key)
            else:
                raise "Leaf should have branch as parent"

    def __DeleteChildOfBranch__(self, child: BaseNode, key: node_key.NodeKey):
        nofSiblings = len(child.Parent.Children.keys())
                
        if nofSiblings == 2: 
            '''
                Only 1 leaf will be left after we delete current one,
                because of that we need to transform the branch 
            '''
            if child.Parent.Parent.Type == node_enums.NodeType.BRANCH:
                self.__DeleteGrandparentIsBranch__(child, key)
            elif child.Parent.Parent.Type == node_enums.NodeType.EXTENSION:
                self.__DeleteGrandparentIsExtension__(child, key)
            else:
                raise "leaf can not be a parent"
        else:
            '''
                We can safely delete just this leaf, since branch will have >=2 children left
                and is still valid branch
            '''
            del child.Parent.Children[self.LastBranchKeyAccessed]

        return True

    def __DeleteGrandparentIsExtension__(self, child: BaseNode, key: node_key.NodeKey):
        sibling = self.__FindSibling__(child, self.LastBranchKeyAccessed)
        if sibling.Type == node_enums.NodeType.LEAF:
            '''
                Parent extension becomes leaf, with key: extKey + branchIndx + leafSiblingKey
            '''
            newLeafKey = node_key.NodeKey(child.Parent.Parent.Key.Key + self.LastBranchKeyAccessed + sibling.Key.Key)
            newLeaf = leaf_node.LeafNode(
                prefix=newLeafKey.GetPrefix(node_enums.NodeType.LEAF),
                keyEnd=newLeafKey,
                value=sibling.Value,
                parent=child.Parent.Parent.Parent
            )

            if child.Parent.Parent.Parent is None:
                self.Root = newLeaf
            else: # 3rd degree parent is branch 
                grandParentBranchIndx = child.Parent.Parent.Parent.GetBranchIndxForParticularNode(child.Parent.Parent)
                child.Parent.Parent.Parent.Children[grandParentBranchIndx] = newLeaf
        elif sibling.Type == node_enums.NodeType.EXTENSION:
            '''
                Merge grandparent extension, branch, and sibling extension into new extension
            '''
            newExtensionKey = node_key.NodeKey(child.Parent.Parent.Key.Key + self.LastBranchKeyAccessed + sibling.Key.Key)
            newExtension = ExtensionNode(
                prefix=newExtensionKey.GetPrefix(node_enums.NodeType.EXTENSION),
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
            newExtensionKey = node_key.NodeKey(child.Parent.Parent.Key.Key + self.LastBranchKeyAccessed)
            newExtension = ExtensionNode(
                prefix=newExtensionKey.GetPrefix(node_enums.NodeType.EXTENSION),
                sharedKey=newExtensionKey,
                branchChild=sibling,
                parent=child.Parent.Parent
            )
            
            if child.Parent.Parent.Parent is None:
                self.Root = newExtension
            else: # 3rd degree parent is branch 
                grandParentBranchIndx = child.Parent.Parent.Parent.GetBranchIndxForParticularNode(child.Parent.Parent)
                child.Parent.Parent.Parent.Children[grandParentBranchIndx] = newExtension


    def __DeleteGrandparentIsBranch__(self, child: BaseNode, key: node_key.NodeKey):
        sibling = self.__FindSibling__(child, self.LastBranchKeyAccessed)
        if sibling.Type == node_enums.NodeType.LEAF:
            '''
                Child.Parent branch becomes leaf, with key branchIndx + sibling.Key
            '''
            newLeafKey = node_key.NodeKey(self.LastBranchKeyAccessed + sibling.Key.Key)
            newLeaf = leaf_node.LeafNode(
                prefix=newLeafKey.GetPrefix(node_enums.NodeType.LEAF),
                keyEnd=newLeafKey,
                parent=child.Parent.Parent,
                value=sibling.Value
            )

            parentBranchIndx = child.Parent.Parent.GetBranchIndxForParticularNode(child.Parent)
            child.Parent.Parent.Children[parentBranchIndx] = newLeaf

        elif sibling.Type == node_enums.NodeType.EXTENSION:
            '''
                Branch get merged with sibling extension
                Sibling extension new key is: branchIndx + extensionOldKey
            '''
            newExtensionKey = node_key.NodeKey(self.LastBranchKeyAccessed + sibling.Key.Key)
            sibling.Key = newExtensionKey
            sibling.Parent = child.Parent.Parent

            parentBranchIndx = child.Parent.Parent.GetBranchIndxForParticularNode(child.Parent)
            child.Parent.Parent.Children[parentBranchIndx] = sibling
        else: # sibling is branch
            '''
                Current branch parent becomes an extension
                Not sure if this is right
            '''
            newExtensionKey = node_key.NodeKey(key.Key)
            newExtension = ExtensionNode(
                prefix=newExtensionKey.GetPrefix(node_enums.NodeType.EXTENSION),
                sharedKey=newExtensionKey,
                branchChild=sibling,
                parent=child.Parent.Parent
            )

            parentBranchIndx = child.Parent.Parent.GetBranchIndxForParticularNode(child.Parent)
            child.Parent.Parent.Children[parentBranchIndx] = newExtension

    def __FindSibling__(self, child: BaseNode, branchIndx: str):
        if child.Parent.Type == node_enums.NodeType.BRANCH:
            for k, v in child.Parent.Children.items():
                if k != branchIndx:
                    return v
            raise "coudln't find sibling"
        else:
            raise "parent is not a branch"