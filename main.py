import random
from models.branch_node import BranchNode
from models.node_enums import NodeValue
from models.node_key import NodeKey
from operations.mpt_trie import MPT
import sha3

def check_for_key(key:str, mpt: MPT):
    val = mpt.Search(NodeKey(key))
    if val is None:
        print(f"There is no value for key {key}")
    else:
        print(f"Value for key {key} is {val.Value}")

def update_for_key(key: str, val: int, mpt:MPT):
    updated = mpt.Update(NodeKey(key), NodeValue(val))
    if updated is None:
        print("Can not update, key is not in trie")
    else:
        print(f"checking is value {val} right for key {key}")
        check_for_key(key, mpt)

def delete_key(key: str, mpt:MPT):
    deleteRes = mpt.Delete(NodeKey(key))
    if deleteRes is None or deleteRes == False:
        print("Failed to delete")
    else:
        print(f"Deleted route with key {key}")

KEY_LENGTH = 10
NOF_NODES = 20
MIN_NODE_VALUE = -100
MAX_NODE_VALUE = -100
NOF_RANDOM_KEY_CHECKS = 5

class InsertValue:
    def __init__(self, key: NodeKey, value: NodeValue) -> None:
        self.Key = key
        self.Value = value

def main():

    insertValues: list[InsertValue] = []
    k = sha3.keccak_512()
    for i in range(NOF_NODES):
        val = random.randint(MIN_NODE_VALUE, MAX_NODE_VALUE)
        k.update(val.to_bytes(4, 'big', signed=True))
        insertValues.append(InsertValue(
            NodeKey(k.hexdigest()),
            NodeValue(val)
        ))

    mpt = MPT.CreateMPT(insertValues[0].Key, insertValues[0].Value)

    for i in range(len(insertValues)):
        if i != 0:
            mpt.Insert(insertValues[i].Key, insertValues[i].Value)

    print()
    for i in range(NOF_RANDOM_KEY_CHECKS):
        print("Key should be in trie")
        check_for_key(insertValues[random.randint(0, len(insertValues)-1)].Key.Key, mpt)

    check_for_key("1111111", mpt)
    # check_for_key("", mpt)

    print()
    for i in range(NOF_RANDOM_KEY_CHECKS):
        print("Key should be in trie")
        update_for_key(insertValues[random.randint(0, len(insertValues)-1)].Key.Key, random.randint(MIN_NODE_VALUE, MAX_NODE_VALUE), mpt)

    # update_for_key("", 234, mpt)

    print()
    for i in range(NOF_RANDOM_KEY_CHECKS):
        print("Key should be in trie")
        delete_key(insertValues[random.randint(0, len(insertValues)-1)].Key.Key, mpt)

    # delete_key("", mpt)


if __name__ == "__main__":
    main()