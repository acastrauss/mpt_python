
from models.base_node import BaseNode
from testing.test_defines import InsertValue
from operations.mpt_trie import MPT
from testing.test_defines import *
import sha3
import random

class TestInit():
    def __init__(self) -> None:
        self.InsertValues: list[InsertValue] = []
        k = sha3.keccak_512()
        for i in range(NOF_NODES):
            val = NodeValue(random.randint(MIN_NODE_VALUE, MAX_NODE_VALUE)) 
            k.update(val.GetBytes())
            self.InsertValues.append(InsertValue(
                NodeKey(k.hexdigest()),
                val
            ))

        BaseNode.instanceId = 0
        self.MPT = MPT.CreateMPT(self.InsertValues[0].Key, self.InsertValues[0].Value)
        for i in range(1, len(self.InsertValues)):
            self.MPT.Insert(self.InsertValues[i].Key, self.InsertValues[i].Value)
        