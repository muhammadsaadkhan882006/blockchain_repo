
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
            "timestamp" : self.timestamp ,
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
        genesis_block = Block(index = 0 , transaction = "Genesis Block" , previous_hash = "0000000000000000");
        self.chain.append(genesis_block)


    def add_transaction(self , sender , receiver , amount):
        transaction_new = {"sender" : sender , "receiver" : receiver , "amount" : amount }
        self.pending_transactions.append(transaction_new)
        return len(self.chain)


    def mine_block(self):
        last_block = self.chain[-1] #this is to get the last block so we use it to take the hash of the last block
        new_block = Block(index = len(self.chain) , transaction = self.pending_transactions , previous_hash = last_block.hash)

        while not new_block.hash.startswith("0000"): # startswith() is a built-in funct for str checks if starts with some prefix 
            new_block.nounce += 1 
            new_block.hash = new_block.calculate_hash() 
        self.chain.append(new_block)
        self.pending_transactions = [] 

    def is_chain_valid(self):
        for i in range(1 , len(self.chain)) :
            current_block = self.chain[i]
            prev_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash() :
                return False 

            if prev_block.hash != current_block.previous_hash :
                return False 

            if not current_block.hash.startswith("0000") :
                return False 

        return True 





