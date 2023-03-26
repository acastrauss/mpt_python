import models.node_enums as node_enums

SIMILARITY_INDEX_NOT_FOUND = -1

class TearedKey:
    def __init__(self, tearedPart: str, partThatLeft: str) -> None:
        self.TearedPart = tearedPart
        self.PartThatLeft = partThatLeft

class NodeKey:
    def __init__(self, key: str) -> None:
        self.Key = key

    def __eq__(self, __o: object) -> bool:
        if (isinstance(__o, self.__class__)):
            return self.Key == __o.Key
        else:
            return False

    def GetPrefix(self, nodeType: node_enums.NodeType) -> node_enums.NodePrefix:
        lenModule = self.GetLen() % 2
        return node_enums.NodePrefix(lenModule + nodeType.value * 2)

    def GetLen(self):
        return len(self.Key)

    def TearApartGivenKeyWithMe(self, key):
        if self.GetLen() > key.GetLen():
            raise "Can not tear appart smaller key with a larger one"
        
        indexOfSimilarity = 0

        for i in range(self.GetLen()):
            if self.Key[i] == key.Key[i]:
                indexOfSimilarity += 1
            else:
                break
        
        return TearedKey(key.Key[:indexOfSimilarity], key.Key[indexOfSimilarity:])

    def GetLastSimilarCharWithGivenKey(self, key):
        lastSimilarIndx = SIMILARITY_INDEX_NOT_FOUND

        for i in range(min(self.GetLen(), key.GetLen())):
            if self.Key[i] == key.Key[i]:
                lastSimilarIndx = i
            else:
                break

        if lastSimilarIndx == SIMILARITY_INDEX_NOT_FOUND:
            raise "no similarity"
        
        return key.Key[lastSimilarIndx]

    def CountSimilaritiesWithKey(self, key):
        cntOfSimilarity = 0

        for i in range(min(self.GetLen(), key.GetLen())):
            if self.Key[i] == key.Key[i]:
                cntOfSimilarity += 1
            else:
                break

        return cntOfSimilarity

    def GetSharedKeyWithGivenKey(self, key):
        sharedKey = NodeKey("")

        for i in range(key.GetLen()):
            if self.Key[i] == key.Key[i]:
                sharedKey.Key += self.Key[i]
            else:
                break

        if sharedKey.GetLen() == 0:
            raise "no shared key"
        
        return sharedKey