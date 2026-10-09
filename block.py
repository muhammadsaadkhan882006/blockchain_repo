
import hashlib
import time
import json

class Block:
    def __init__(self ,index , transaction , previous_hash , nounce = 0 ):
        self.index = index
        self.timestamp = time.time()
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nounce = nounce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_dict = {
            "index" : self.index ,
            "timestamp" : self.time ,
            "transaction" : self.transaction ,
            "previous hash" : self.previous_hash ,
            "nounce" : self.nounce ,
        }
        data_string = json.dumps(block_dict , sort_keys= True) ;
        return hashlib.sha256(data_string.encode()).hexdigest() 

    
class Blockchain:
    def __init__(self):
        self.chain = [] 
        self.pending_transactions = []
        self.create_genesis_block() 
    def create_genesis_block(self):
        genesis_block = Block(index = 0 , taransaction = "Genesis Block" , previous_hash = "0000000000000000");
        self.chain.append(genesis_block)



example_dic = {2 :"saad" , 1 : "20"}
print(json.dumps(example_dic  ))