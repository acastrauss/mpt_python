import random
from models.branch_node import BranchNode
from models.node_enums import NodeValue
from models.node_key import NodeKey
from operations.mpt_trie import MPT

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
KEY_START = 'a'
MIN_NODE_VALUE = -100
MAX_NODE_VALUE = -100
NOF_RANDOM_KEY_CHECKS = 5

def main():

    keys = []

    for i in range(NOF_NODES):
        key = ''
        for j in range(KEY_LENGTH):
            key += BranchNode.possibleBranchIndxs[random.randint(0, len(BranchNode.possibleBranchIndxs)-1)]
        if not(key in keys):
            keys.append(key)

    mpt = MPT.CreateMPT(NodeKey(keys[0]), NodeValue(1))

    for i in range(len(keys)):
        if i != 0:
            mpt.Insert(NodeKey(keys[i]), NodeValue(random.randint(MIN_NODE_VALUE, MAX_NODE_VALUE)))

    print()
    for i in range(NOF_RANDOM_KEY_CHECKS):
        print("Key should be in trie")
        check_for_key(keys[random.randint(0, len(keys)-1)], mpt)

    check_for_key("1111111", mpt)
    # check_for_key("", mpt)

    print()
    for i in range(NOF_RANDOM_KEY_CHECKS):
        print("Key should be in trie")
        update_for_key(keys[random.randint(0, len(keys)-1)], random.randint(MIN_NODE_VALUE, MAX_NODE_VALUE), mpt)

    # update_for_key("", 234, mpt)

    print()
    for i in range(NOF_RANDOM_KEY_CHECKS):
        print("Key should be in trie")
        delete_key(keys[random.randint(0, len(keys)-1)], mpt)

    # delete_key("", mpt)


if __name__ == "__main__":
    main()