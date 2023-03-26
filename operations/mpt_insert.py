from models.base_node import BaseNode
from models.branch_node import BranchNode
from models.extension_node import ExtensionNode
from models.leaf_node import LeafNode
from models.node_enums import NodeType, NodeValue
from models.node_key import NodeKey, TearedKey

class MPTInsert:
    def __init__(self, mpt, updateOps) -> None:
        self.MPT = mpt
        self.UpdateOps = updateOps
    
    def Insert(self, key: NodeKey, value: NodeValue):
        self.__GetLastSimilarNode__(self.MPT.Root, key)

        if self.MPT.LastSimilarNode.Type == NodeType.LEAF:
            '''
                Make extension from leaf, and add branch as a child with
                2 children, one with current leaf sliced key
                and other with new sliced key
                If there are no similarities between keys, create just a branch, no extension
            '''
            similiaritiesNum = self.MPT.LastSimilarNode.Key.CountSimilaritiesWithKey(NodeKey(f"{self.MPT.TearedKey.TearedPart}{self.MPT.TearedKey.PartThatLeft}"))
            if self.MPT.LastSimilarNode.Key.Key == f"{self.MPT.TearedKey.TearedPart}{self.MPT.TearedKey.PartThatLeft}":
                self.UpdateOps.Update(key, value)
                return
            
            if similiaritiesNum > 0:
                sharedKey = self.MPT.LastSimilarNode.Key.GetSharedKeyWithGivenKey(NodeKey(f"{self.MPT.TearedKey.TearedPart}{self.MPT.TearedKey.PartThatLeft}"))

                newExtension = ExtensionNode(
                    prefix=sharedKey.GetPrefix(NodeType.EXTENSION),
                    sharedKey=sharedKey,
                    branchChild=None,
                    parent=self.MPT.LastSimilarNode.Parent
                )

                newBranch = BranchNode(
                    children={},
                    parent=newExtension,
                    value=None
                )

                newExtension.BranchChild = newBranch

                lsnKeyLen = self.MPT.LastSimilarNode.Key.GetLen()
                newLeaf1Key = NodeKey(
                    self.MPT.LastSimilarNode.Key.Key[lsnKeyLen-len(self.MPT.TearedKey.PartThatLeft):]
                )

                fixedNewLeaf1Key = NodeKey(newLeaf1Key.Key[1:])
                newBranch.Children[newLeaf1Key.Key[0]] = LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(NodeType.LEAF),
                    keyEnd=fixedNewLeaf1Key,
                    value=self.MPT.LastSimilarNode.Value,
                    parent=newBranch
                )

                newLeaf2Key = self.MPT.TearedKey.PartThatLeft
                fixedNewLeaf2Key = NodeKey(newLeaf2Key[1:])
                newBranch.Children[newLeaf2Key[0]] = LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(NodeType.LEAF),
                    keyEnd=fixedNewLeaf2Key,
                    value=value,
                    parent=newBranch
                )

                if self.MPT.LastSimilarNode.Parent == None:
                    self.MPT.Root = newExtension
                elif self.MPT.LastSimilarNode.Parent.Type == NodeType.BRANCH:
                    self.MPT.LastSimilarNode.Parent.Children[self.MPT.LastBranchKeyAccessed] = newExtension
                else:
                    raise "only branch can be a parent of a leaf"
            else: # just create a branch
                newBranch = BranchNode(
                    children={},
                    parent=self.MPT.LastSimilarNode.Parent,
                    value=None
                )

                lsnKeyLen = self.MPT.LastSimilarNode.Key.GetLen()
                newLeaf1Key = NodeKey(
                    self.MPT.LastSimilarNode.Key.Key[lsnKeyLen-len(self.MPT.TearedKey.PartThatLeft):]
                )

                fixedNewLeaf1Key = NodeKey(newLeaf1Key.Key[1:])
                newBranch.Children[newLeaf1Key.Key[0]] = LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(NodeType.LEAF),
                    keyEnd=fixedNewLeaf1Key,
                    value=self.MPT.LastSimilarNode.Value,
                    parent=newBranch
                )

                newLeaf2Key = self.MPT.TearedKey.PartThatLeft
                fixedNewLeaf2Key = NodeKey(newLeaf2Key[1:])
                newBranch.Children[newLeaf2Key[0]] = LeafNode(
                    prefix=fixedNewLeaf1Key.GetPrefix(NodeType.LEAF),
                    keyEnd=fixedNewLeaf2Key,
                    value=value,
                    parent=newBranch
                )

                if self.MPT.LastSimilarNode.Parent == None:
                    self.MPT.Root = newBranch
                elif self.MPT.LastSimilarNode.Parent.Type == NodeType.BRANCH:
                    self.MPT.LastSimilarNode.Parent.Children[self.MPT.LastBranchKeyAccessed] = newBranch
                else:
                    raise "only branch can be a parent of a leaf"

        elif self.MPT.LastSimilarNode.Type == NodeType.BRANCH:
            if not self.MPT.LastSimilarNode.IsKeyInBranch(NodeKey(self.MPT.TearedKey.PartThatLeft)):
                newLeafKey = NodeKey(self.MPT.TearedKey.PartThatLeft[1:])
                self.MPT.LastSimilarNode.Children[self.MPT.TearedKey.PartThatLeft[0]] = LeafNode(
                    prefix=newLeafKey.GetPrefix(NodeType.LEAF),
                    keyEnd=newLeafKey,
                    parent=self.MPT.LastSimilarNode,
                    value=value
                )
            else:
                self.UpdateOps.Update(key, value)
            
        else:
            tempKey = NodeKey(f"{self.MPT.TearedKey.TearedPart}{self.MPT.TearedKey.PartThatLeft}")
            similiaritiesNum = self.MPT.LastSimilarNode.Key.CountSimilaritiesWithKey(tempKey)
            
            if similiaritiesNum > 0: # make new extension from two keys
                newCommonKey: NodeKey = self.MPT.LastSimilarNode.Key.GetSharedKeyWithGivenKey(tempKey)

                newCommonExtension = ExtensionNode(
                    prefix=newCommonKey.GetPrefix(NodeType.EXTENSION),
                    sharedKey=newCommonKey,
                    parent=self.MPT.LastSimilarNode.Parent,
                    branchChild=None
                )

                newBranch = BranchNode(
                    children={},
                    parent=newCommonExtension,
                    value=None
                )

                newCommonExtension.BranchChild = newBranch

                newLeafKey = newCommonKey.TearApartGivenKeyWithMe(NodeKey(self.MPT.TearedKey.PartThatLeft))
                nlkFixed = NodeKey(newLeafKey.PartThatLeft[1:])

                newBranch.Children[newLeafKey.PartThatLeft[0]] = LeafNode(
                    prefix=nlkFixed.GetPrefix(NodeType.LEAF),
                    keyEnd=nlkFixed,    
                    parent=newBranch,
                    value=value
                )

                prevExtTearedKey = newCommonKey.TearApartGivenKeyWithMe(self.MPT.LastSimilarNode.Key)

                if len(prevExtTearedKey.PartThatLeft) == 1:
                    newBranch.Children[prevExtTearedKey.PartThatLeft[0]] = self.MPT.LastSimilarNode.BranchChild
                else:
                    tempKey1 = NodeKey(newCommonKey.Key + prevExtTearedKey.PartThatLeft[0])
                    keyToUse1 = tempKey1.TearApartGivenKeyWithMe(prevExtTearedKey.PartThatLeft)
                    ktu = NodeKey(keyToUse1.PartThatLeft)
                    newChildExt1 = ExtensionNode(
                        prefix=ktu.GetPrefix(NodeType.EXTENSION),
                        branchChild=self.MPT.LastSimilarNode.BranchChild,
                        parent=newBranch,
                        sharedKey=ktu
                    )
                    newBranch.Children[prevExtTearedKey.PartThatLeft[0]] = newChildExt1

                if self.MPT.LastSimilarNode.Parent == None:
                    self.MPT.Root = newCommonExtension
                elif self.MPT.LastSimilarNode.Parent.Type == NodeType.BRANCH: 
                    self.MPT.LastSimilarNode.Parent.Children[self.MPT.LastBranchKeyAccessed] = newCommonExtension
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
                    parent=self.MPT.LastSimilarNode.Parent,
                    value=None
                )

                if self.MPT.LastSimilarNode.Parent == None:
                    self.MPT.Root = newBranch
                elif self.MPT.LastSimilarNode.Parent.Type == NodeType.BRANCH: 
                    self.MPT.LastSimilarNode.Parent.Children[self.MPT.LastBranchKeyAccessed] = newBranch
                else:
                    raise "Extension has wrong parent"

                if self.MPT.LastSimilarNode.Key.GetLen() == 1:
                    newBranch.Children[self.MPT.LastSimilarNode.Key.Key[0]] = self.MPT.LastSimilarNode.BranchChild
                    self.MPT.LastSimilarNode.BranchChild.Parent = newBranch
                else:
                    branchIndx = self.MPT.LastSimilarNode.Key.Key[0]
                    newExtKey = NodeKey(self.MPT.LastSimilarNode.Key.Key[1:])
                    newExtension = ExtensionNode(
                        prefix=newExtKey.GetPrefix(NodeType.EXTENSION),
                        sharedKey=newExtKey,
                        branchChild=self.MPT.LastSimilarNode.BranchChild,
                        parent=newBranch
                    )
                    newBranch.Children[branchIndx] = newExtension
                    self.MPT.LastSimilarNode.BranchChild.Parent = newExtension

                newLeafKey = NodeKey(tempKey.Key[1:])
                leafBranchIndx = tempKey.Key[0]
                newLeaf = LeafNode(
                    prefix=newLeafKey.GetPrefix(NodeType.LEAF),
                    keyEnd=newLeafKey,
                    value=value,
                    parent=newBranch
                )
                newBranch.Children[leafBranchIndx] = newLeaf

    def __GetLastSimilarNode__(self, nodeToCompareTo, key: NodeKey):
        tearedKey:TearedKey = nodeToCompareTo.TearApartGivenKeyWithMine(key)

        if nodeToCompareTo.Type == NodeType.BRANCH:
            if nodeToCompareTo.IsKeyInBranch(key):
                branchIndx = key.Key[0]
                self.MPT.LastBranchKeyAccessed = branchIndx
                self.__GetLastSimilarNode__(nodeToCompareTo.Children[branchIndx], NodeKey(tearedKey.PartThatLeft))
            else:
                self.MPT.LastSimilarNode = nodeToCompareTo
                self.MPT.TearedKey = tearedKey
                
        elif nodeToCompareTo.Type == NodeType.EXTENSION:
            if key.Key.startswith(nodeToCompareTo.Key.Key):
                self.__GetLastSimilarNode__(nodeToCompareTo.BranchChild, NodeKey(tearedKey.PartThatLeft))
            else:
                self.MPT.LastSimilarNode = nodeToCompareTo # key doesn't start with extension key
                self.MPT.TearedKey = tearedKey
        else:
            self.MPT.LastSimilarNode = nodeToCompareTo
            self.MPT.TearedKey = tearedKey