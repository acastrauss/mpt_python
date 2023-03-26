import unittest
from models.node_key import NodeKey
from testing.test_init import TestInit

class TestMPTSearch(unittest.TestCase):

    def test_search(self):
        testInit = TestInit()

        for i in range(len(testInit.InsertValues)):
            val = testInit.MPT.Search(testInit.InsertValues[i].Key)
            self.assertTrue(val == testInit.InsertValues[i].Value)

        val = testInit.MPT.Search(NodeKey("KeyNotInTrie"))
        self.assertIsNone(val)