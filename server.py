import sys
import requests
from flask import Flask, jsonify, request
from Block import Block
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

# 1. View local blockchain
@app.route('/blockchain', methods=['GET'])
def get_chain():
    chain_data = [
        {
            "index": block.index,
            "timestamp": block.timestamp,
            "transaction": block.transaction,
            "previous_hash": block.previous_hash,
            "nounce": block.nounce,
            "hash": block.hash,
        }
        for block in blockchain.chain
    ]
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200

# 2. View pending transactions
@app.route('/transactions', methods=['GET'])
def get_pending_transactions():
    return jsonify({"pending_transactions": blockchain.pending_transactions}), 200

# 3. Create & Broadcast Transaction
@app.route('/transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required = ["sender", "receiver", "amount"]
    if not tx_data or not all(k in tx_data for k in required):
        return jsonify({"message": "Missing transaction data"}), 400

    blockchain.add_transaction(tx_data["sender"], tx_data["receiver"], tx_data["amount"])

    # Broadcast to peers (flag prevents infinite loops)
    if not tx_data.get("broadcasted", False):
        tx_data["broadcasted"] = True
        for node in blockchain.nodes:
            try:
                requests.post(f"{node}/transaction", json=tx_data, timeout=2)
            except requests.exceptions.RequestException:
                pass

    return jsonify({"message": "Transaction added successfully"}), 201

# 4. Mine Block & Broadcast
@app.route('/mine', methods=['POST', 'GET'])
def mine():
    new_block = blockchain.mine_block()
    block_data = {
        "index": new_block.index,
        "timestamp": new_block.timestamp,
        "transaction": new_block.transaction,
        "previous_hash": new_block.previous_hash,
        "nounce": new_block.nounce,
        "hash": new_block.hash,
    }

    # Broadcast newly mined block to all registered nodes
    for node in list(blockchain.nodes):
        try:
            requests.post(f"{node}/block/receive", json=block_data, timeout=2)
        except requests.exceptions.RequestException:
            pass

    return jsonify({"message": "Block mined and broadcasted", "block": block_data}), 200

# 5. Receive Broadcasted Block
@app.route('/block/receive', methods=['POST'])
def receive_block():
    block_data = request.get_json()
    last_block = blockchain.chain[-1]

    # Validate block connection and PoW before adding
    if block_data["previous_hash"] == last_block.hash and block_data["hash"].startswith("0000"):
        new_block = Block(
            index=block_data["index"],
            transaction=block_data["transaction"],
            previous_hash=block_data["previous_hash"],
            nounce=block_data["nounce"],
        )
        new_block.timestamp = block_data["timestamp"]
        new_block.hash = block_data["hash"]

        blockchain.chain.append(new_block)
        blockchain.pending_transactions = []
        return jsonify({"message": "Block accepted"}), 201

    return jsonify({"message": "Block rejected"}), 400

# 6. Register Peer Nodes
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    data = request.get_json()
    nodes = data.get("nodes")
    if not nodes:
        return jsonify({"message": "Please supply a valid list of node URLs"}), 400

    for node in nodes:
        blockchain.nodes.add(node)

    return jsonify({"message": "Nodes registered", "total_nodes": list(blockchain.nodes)}), 201

# 7. Consensus / Chain Resolution
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    local_valid = blockchain.is_chain_valid()
    max_length = len(blockchain.chain)
    new_chain = None

    for node in list(blockchain.nodes):
        try:
            response = requests.get(f"{node}/blockchain", timeout=2)
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                # Replace if received chain is strictly longer, 
                # OR if local chain is invalid and received chain is equal length & valid
                if blockchain.is_chain_valid(chain):
                    if length > max_length or (length == max_length and not local_valid):
                        max_length = length
                        new_chain = chain
        except requests.exceptions.RequestException:
            pass

    if new_chain:
        reconstructed = []
        for b in new_chain:
            block_obj = Block(b["index"], b["transaction"], b["previous_hash"], b["nounce"])
            block_obj.timestamp = b["timestamp"]
            block_obj.hash = b["hash"]
            reconstructed.append(block_obj)

        blockchain.chain = reconstructed
        return jsonify({"message": "Chain replaced with valid chain from network"}), 200

    return jsonify({"message": "Current chain is authoritative"}), 200


# 8. Tamper with a block (for testing/demo)
@app.route('/tamper', methods=['POST'])
def tamper_block():
    if len(blockchain.chain) > 1:
        # Manually alter the transactions in Block 1
        blockchain.chain[1].transaction = [{'amount': 10000, 'receiver': 'Hacker', 'sender': 'Alice'}]
        return jsonify({"message": "Block 1 has been tampered with!"}), 200
    return jsonify({"message": "No blocks available to tamper"}), 400

# 9. Validate local chain
@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({"is_valid": is_valid}), 200

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    app.run(host='0.0.0.0', port=port, debug=True)