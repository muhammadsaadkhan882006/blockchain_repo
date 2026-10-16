import requests

NODE1 = "http://localhost:5001"
NODE2 = "http://localhost:5002"

print("--- 1. CHECKING INITIAL VALIDITY ON NODE 2 ---")
res = requests.get(f"{NODE2}/validate").json()
print("Node 2 Chain Valid?", res["is_valid"])

print("\n--- 2. TAMPERING WITH BLOCK 1 ON NODE 2 ---")
tamper_res = requests.post(f"{NODE2}/tamper").json()
print("Tamper Result:", tamper_res["message"])

print("\n--- 3. CHECKING VALIDITY ON NODE 2 AFTER TAMPERING ---")
res = requests.get(f"{NODE2}/validate").json()
print("Node 2 Chain Valid?", res["is_valid"])  # Expected: False

print("\n--- 4. RUNNING CONSENSUS RECOVERY ON NODE 2 ---")
requests.get(f"{NODE2}/nodes/resolve")

print("\n--- 5. CHECKING VALIDITY ON NODE 2 AFTER RECOVERY ---")
res = requests.get(f"{NODE2}/validate").json()
print("Node 2 Chain Valid After Recovery?", res["is_valid"])  # Expected: True