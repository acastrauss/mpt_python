from models.node_enums import NodeValue
from models.node_key import NodeKey
from operations.mpt_trie import MPT

def main():
    mpt = MPT.CreateMPT(NodeKey("a711355"), NodeValue(1))
    mpt.Insert(NodeKey("a7ad337"), NodeValue(22))
    mpt.Insert(NodeKey("a4ad337"), NodeValue(22))
    mpt.Insert(NodeKey("a7ad567"), NodeValue(22))
    mpt.Insert(NodeKey("a4a4337"), NodeValue(22))

if __name__ == "__main__":
    main()