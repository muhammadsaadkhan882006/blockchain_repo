import requests
import json

NODE1 = "http://localhost:5001"
NODE2 = "http://localhost:5002"
NODE3 = "http://localhost:5003"

print("--- 1. REGISTERING PEERS ---")
# Register Node 2 and Node 3 with Node 1
requests.post(f"{NODE1}/nodes/register", json={"nodes": [NODE2, NODE3]})
# Register Node 1 and Node 3 with Node 2
requests.post(f"{NODE2}/nodes/register", json={"nodes": [NODE1, NODE3]})
# Register Node 1 and Node 2 with Node 3
requests.post(f"{NODE3}/nodes/register", json={"nodes": [NODE1, NODE2]})
print("Nodes registered with each other successfully.\n")

print("--- 2. CREATING & BROADCASTING TRANSACTION ON NODE 1 ---")
tx_payload = {
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 100
}
response = requests.post(f"{NODE1}/transaction", json=tx_payload)
print("Node 1 Response:", response.json())

# Verify pending pool on Node 2 to confirm transaction broadcasted
pending_node2 = requests.get(f"{NODE2}/transactions").json()
print("Node 2 Pending Transactions Pool:", pending_node2, "\n")

print("--- 3. MINING BLOCK ON NODE 1 ---")
mine_response = requests.post(f"{NODE1}/mine")
print("Mining Response:", mine_response.json(), "\n")

print("--- 4. CHECKING BLOCKCHAIN LEDGERS ON ALL NODES ---")
for name, url in [("Node 1", NODE1), ("Node 2", NODE2), ("Node 3", NODE3)]:
    res = requests.get(f"{url}/blockchain").json()
    print(f"{name} Chain Length: {res['length']} | Latest Hash: {res['chain'][-1]['hash']}")

print("--- 5. SYNCHRONIZING NODES VIA CONSENSUS ---")
requests.get(f"{NODE2}/nodes/resolve")
requests.get(f"{NODE3}/nodes/resolve")

for name, url in [("Node 1", NODE1), ("Node 2", NODE2), ("Node 3", NODE3)]:
    res = requests.get(f"{url}/blockchain").json()
    print(f"{name} Chain Length: {res['length']} | Latest Hash: {res['chain'][-1]['hash']}")