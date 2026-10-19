# Modular P2P Blockchain Implementation

A fully functional, modular Peer-to-Peer (P2P) Blockchain system built from scratch in Python using Flask RESTful APIs. This project implements core blockchain mechanics including SHA-256 hashing, Proof-of-Work (PoW) consensus, transaction/block network broadcasting, and automated chain resolution for tamper resilience.

---

## Features

- **Deterministic Hashing & Genesis Standardization:** Uses SHA-256 with standard serialization (`json.dumps` with sorted keys) and a fixed Genesis timestamp (`timestamp=0`) to ensure consistent root hashes across nodes.
- **Proof-of-Work (PoW):** Nonce-based mining targeting a leading prefix (`"0000"`).
- **Modular Project Structure:** Clean separation of concerns across data types, chain logic, and API networking layer.
- **P2P Flask Network:** Multi-node communication running across independent ports (`5001`, `5002`, `5003`).
- **Broadcast Protocol:** Automatic propagation of new transactions and mined blocks across registered peers.
- **Consensus & Resilience:** Resolves fork conflicts and repairs tampered/corrupted local ledgers using the longest valid chain rule.

---

## Project Structure

```text
.
├── Block.py             # Defines the Block structure, timestamping, and SHA-256 hashing
├── blockchain.py        # Core Blockchain class (chain management, mining, validation, consensus)
├── transaction.py       # Transaction data structure helper
├── server.py            # Flask API server handling network routes and peer communication
├── test_script.py       # Standalone test script for core blockchain logic
├── demo_network.py      # Automated network setup, transaction broadcasting, and block propagation
└── test_tampering.py    # Automated test verifying tamper detection and consensus recovery
```

---

## Prerequisites & Installation

### Requirements
- Python 3.8+
- `pip` (Python package installer)

### Setup
1. Clone or download the repository to your local machine.
2. Install the required Python dependencies:

```bash
pip install flask requests
```

---

## API Endpoints Reference (`server.py`)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/blockchain` | `GET` | Returns the local node's full blockchain ledger. |
| `/transactions` | `GET` | Returns the pool of pending transactions. |
| `/transaction` | `POST` | Creates a new transaction and broadcasts it to registered peers. |
| `/mine` | `POST` / `GET` | Mines pending transactions into a new block and broadcasts it. |
| `/block/receive` | `POST` | Receives and validates a broadcasted block from a peer. |
| `/nodes/register` | `POST` | Registers peer node URLs into the node network set. |
| `/nodes/resolve` | `GET` | Runs consensus algorithm to synchronize with the longest valid chain. |
| `/tamper` | `POST` | (Demo) Corrupts local block data to simulate a malicious attack. |
| `/validate` | `GET` | Checks the cryptographic integrity of the local blockchain. |

---

## How to Run & Test

### 1. Core Blockchain Verification
Test standalone mining and validation without network interaction:

```bash
python test_script.py
```

### 2. Running a Multi-Node P2P Network
Open 3 separate terminal instances in your editor and launch a node in each:

- **Terminal 1:** `python server.py 5001`
- **Terminal 2:** `python server.py 5002`
- **Terminal 3:** `python server.py 5003`

### 3. P2P Network Synchronization Demo
Open a **4th terminal** and run the network demonstration script:

```bash
python demo_network.py
```
*This registers peers automatically, broadcasts transactions, mines a block on Node 1, and verifies that all 3 nodes synchronized the new block (`Chain Length: 2`).*

### 4. Tamper Detection & Recovery Test
Run the automated resilience test in the 4th terminal:

```bash
python test_tampering.py
```

**Expected Flow:**
1. Validates Node 2 (`True`).
2. Tampers with Node 2's Block 1 transactions.
3. Re-validates Node 2 (`False` - corruption detected).
4. Executes `/nodes/resolve` consensus query on Node 2.
5. Re-validates Node 2 (`True` - chain repaired from Node 1/Node 3 peers).