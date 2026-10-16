
import hashlib
import time
import json

class Block:
    def __init__(self, index, transaction, previous_hash, nounce=0, timestamp=None):
        self.index = index
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nounce = nounce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_dict = {
            "index" : self.index ,
            "timestamp" : self.timestamp ,
            "transaction" : self.transaction ,
            "previous hash" : self.previous_hash ,
            "nounce" : self.nounce ,
        }
        data_string = json.dumps(block_dict , sort_keys= True) ;
        return hashlib.sha256(data_string.encode()).hexdigest() 

    






