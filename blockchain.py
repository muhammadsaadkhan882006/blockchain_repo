from Block import Block


class Blockchain:
    def __init__(self):
        self.chain = [] 
        self.pending_transactions = []
        self.nodes = set()  # We will use this set to store peer node URLs (e.g., 'http://localhost:5002')
        self.create_genesis_block() 

    def create_genesis_block(self):
        # Setting timestamp=0 ensures every node computes the exact same Genesis hash
        genesis_block = Block(
            index=0, 
            transaction="Genesis Block", 
            previous_hash="0000000000000000", 
            timestamp=0
        )
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount):
        transaction_new = {"sender": sender, "receiver": receiver, "amount": amount}
        self.pending_transactions.append(transaction_new)
        return len(self.chain)

    def mine_block(self):
        last_block = self.chain[-1]
        new_block = Block(index=len(self.chain), transaction=self.pending_transactions, previous_hash=last_block.hash)

        while not new_block.hash.startswith("0000"):
            new_block.nounce += 1 
            new_block.hash = new_block.calculate_hash() 

        self.chain.append(new_block)
        self.pending_transactions = [] 
        return new_block

    def is_chain_valid(self, chain=None):
        if chain is None:
            chain = self.chain

        for i in range(1, len(chain)):
            current = chain[i]
            prev = chain[i-1]

            # Re-instantiate Block if raw dict passed during network sync
            if isinstance(current, dict):
                current_hash = current['hash']
                prev_hash = prev['hash'] if isinstance(prev, dict) else prev.hash
                if not current_hash.startswith("0000") or current['previous_hash'] != prev_hash:
                    return False
            else:
                if current.hash != current.calculate_hash():
                    return False
                if prev.hash != current.previous_hash:
                    return False
                if not current.hash.startswith("0000"):
                    return False

        return True