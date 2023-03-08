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
        self.GetLastSimilarNode(self.Root, key)

        if self.LastSimilarNode.Type == node_enums.NodeType.LEAF:
            '''
                Make extension from leaf, and add branch as a child with
                2 children, one with current leaf sliced key
                and other with new sliced key
            '''
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
                value=value,
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
                raise "Branch already has node with that key"
            
        else:
            tempKey = node_key.NodeKey(f"{self.TearedKey.TearedPart}{self.TearedKey.PartThatLeft}")
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

    def GetLastSimilarNode(self, nodeToCompareTo, key: node_key.NodeKey):
        tearedKey:node_key.TearedKey = nodeToCompareTo.TearApartGivenKeyWithMine(key)

        if nodeToCompareTo.Type == node_enums.NodeType.BRANCH:
            if nodeToCompareTo.IsKeyInBranch(key):
                branchIndx = key.Key[0]
                self.LastBranchKeyAccessed = branchIndx
                self.GetLastSimilarNode(nodeToCompareTo.Children[branchIndx], node_key.NodeKey(tearedKey.PartThatLeft))
            else:
                self.LastSimilarNode = nodeToCompareTo
                self.TearedKey = tearedKey
                
        elif nodeToCompareTo.Type == node_enums.NodeType.EXTENSION:
            if key.Key.startswith(nodeToCompareTo.Key.Key):
                self.GetLastSimilarNode(nodeToCompareTo.BranchChild, node_key.NodeKey(tearedKey.PartThatLeft))
            else:
                self.LastSimilarNode = nodeToCompareTo
                self.TearedKey = tearedKey
        else:
            lastSimilar = nodeToCompareTo

            if nodeToCompareTo.Key.CountSimilaritiesWithKey(key) == node_key.NO_SIMILARITY_BETWEEN_KEYS:
                lastSimilar = nodeToCompareTo.Parent
            
            self.LastSimilarNode = lastSimilar
            self.TearedKey = tearedKey
            # self.KeyDifference = tearedKey
