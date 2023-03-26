from models.branch_node import BranchNode
from models.node_enums import NodeValue
from models.node_key import NodeKey
from operations.mpt_trie import MPT
from testing.test_delete import TestMPTDelete

from testing.test_insert import TestMPTInsert
from testing.test_search import TestMPTSearch
from testing.test_update import TestMPTUpdate

def main():
    testSearch = TestMPTSearch()
    testSearch.test_search()

    testInsert = TestMPTInsert()
    testInsert.test_insert()

    testDelete = TestMPTDelete()
    testDelete.test_delete()

    testUpdate = TestMPTUpdate()
    testUpdate.test_update()



if __name__ == "__main__":
    main()