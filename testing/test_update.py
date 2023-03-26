import unittest
from models.node_key import NodeKey
from testing.test_defines import MAX_NODE_VALUE, MIN_NODE_VALUE

from testing.test_init import TestInit
from models.node_enums import NodeValue
import sha3
import random


class TestMPTUpdate(unittest.TestCase):

    def test_update(self):
        testInit = TestInit()

        for i in range(len(testInit.InsertValues)):
            newValue = NodeValue(random.randint(MIN_NODE_VALUE, MAX_NODE_VALUE))
            updateVal = testInit.MPT.Update(testInit.InsertValues[i].Key, newValue)
            self.assertIsNotNone(updateVal)

            foundVal = testInit.MPT.Search(testInit.InsertValues[i].Key)
            self.assertIsNotNone(foundVal)
            self.assertTrue(foundVal == newValue)

        failKey = NodeKey("KeyNotInTrie")
        failedUpdateVal = testInit.MPT.Update(failKey, newValue)
        self.assertIsNone(failedUpdateVal)
        foundVal = testInit.MPT.Search(failKey)
        self.assertIsNone(foundVal)





