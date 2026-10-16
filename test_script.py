from Block import Block
from transaction import Transaction
from blockchain import Blockchain

# 1. Initialize the blockchain
my_blockchain = Blockchain()

print("Genesis block created!")
print(f"Genesis Hash: {my_blockchain.chain[0].hash}\n")

# 2. Add test transactions
my_blockchain.add_transaction(sender="Alice", receiver="Bob", amount=50)
my_blockchain.add_transaction(sender="Bob", receiver="Charlie", amount=25)

# 3. Mine a new block
print("Mining Block 1...")
mined_block = my_blockchain.mine_block()
print(f"Block 1 Mined! Hash: {mined_block.hash}, Nonce: {mined_block.nounce}\n")

# 4. Check if the blockchain is valid
print("Is the blockchain valid?", my_blockchain.is_chain_valid())

# 5. Display all blocks in the chain
print("\n--- Current Blockchain Ledger ---")
for block in my_blockchain.chain:
    print(f"Block #{block.index}")
    print(f"  Transactions : {block.transaction}")
    print(f"  Previous Hash: {block.previous_hash}")
    print(f"  Current Hash : {block.hash}")
    print(f"  Nonce        : {block.nounce}\n")