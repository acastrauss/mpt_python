import unittest
from models.node_key import NodeKey

from testing.test_init import TestInit


class TestMPTInsert(unittest.TestCase):
    
    def test_insert(self):
        testInit = TestInit()

        for i in range(len(testInit.InsertValues)):
            val = testInit.MPT.Search(testInit.InsertValues[i].Key)
            self.assertIsNotNone(val)
            self.assertTrue(val == testInit.InsertValues[i].Value)

