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

def main():
    mpt = MPT.CreateMPT(NodeKey("a711355"), NodeValue(1))
    mpt.Insert(NodeKey("a7ad337"), NodeValue(22))
    mpt.Insert(NodeKey("a4ad337"), NodeValue(23))
    mpt.Insert(NodeKey("a7ad567"), NodeValue(24))
    mpt.Insert(NodeKey("a4a4337"), NodeValue(255))

    check_for_key("a711355", mpt)
    check_for_key("1111111", mpt)
    check_for_key("", mpt)

    update_for_key("a711355", 234, mpt)
    update_for_key("", 234, mpt)

    delete_key("a4ad337", mpt)
    delete_key("", mpt)


if __name__ == "__main__":
    main()