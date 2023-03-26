import unittest
from models.node_key import NodeKey

from testing.test_init import TestInit


class TestMPTDelete(unittest.TestCase):

    def test_delete(self):
        testInit = TestInit()

        for i in range(len(testInit.InsertValues)):
            found = testInit.MPT.Search(testInit.InsertValues[i].Key)
            
            if found is None:
                '''
                    There is a possibility that insert values are duplicates
                    So if value is already deleted test needs to check if it exists in Trie
                '''
                continue
            
            deleteRes = testInit.MPT.Delete(testInit.InsertValues[i].Key)
            self.assertTrue((deleteRes is not None) and (deleteRes != False))
            found = testInit.MPT.Search(testInit.InsertValues[i].Key)

            self.assertIsNone(found)

        failedDeleteRes = testInit.MPT.Delete(NodeKey("KeyNotInTrie"))
        self.assertTrue(failedDeleteRes is None or failedDeleteRes == False)