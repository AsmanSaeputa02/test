import datetime
import hashlib
import json
from flask import Flask, jsonify, render_template

class Blockchain:
    def __init__(self):
        self.chain = []  # List to store blocks
        self.transaction = 0
        self.create_block(nonce=1, previous_hash="0")

    def create_block(self, nonce, previous_hash):
        current_time = datetime.datetime.now()
        next_five_minutes = (current_time.minute // 5 + 1) * 5
        timestamp_in_future = current_time.replace(minute=next_five_minutes, second=0, microsecond=0)

        # Check if there is a recent block and if there are changes
        if len(self.chain) > 0:
            previous_block = self.get_previous_block()
            if (
                previous_block["data"] == self.transaction
                and previous_block["nonce"] == nonce
                and previous_block["previous_hash"] == previous_hash
            ):
                print("No changes in data, nonce, or previous hash. Block not created.")
                return None

        block = {
            "index": len(self.chain) + 1,
            "data": self.transaction,
            "timestamp": str(timestamp_in_future.strftime("%Y-%m-%d %H:%M:%S")),
            "nonce": nonce,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        print(f"Block {block['index']} created at timestamp: {block['timestamp']}")
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()

    def proof_of_work_easy(self, previous_nonce):
        new_nonce = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    def proof_of_work_hard(self, previous_nonce):
        new_nonce = 1
        check_proof = False
        target_zeros = 5

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:target_zeros] == "0" * target_zeros:
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    def is_chain_valid(self, chain):
        if not chain:
            return False

        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False

            previous_nonce = previous_block["nonce"]
            nonce = block["nonce"]
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()

            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True


blockchain = Blockchain()
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/get_chain')
def get_chain():
    response_chain = []
    for block in blockchain.chain:
        response_chain.append({
            "index": block["index"],
            "data": block["data"],
            "timestamp": block["timestamp"],
            "nonce": block["nonce"],
            "previous_hash": block["previous_hash"],
            "hash": blockchain.hash(block)  # Add hash to the response
        })

    response = {
        "chain": response_chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

# Easy mode mining
@app.route('/mining/easy')
def mining_block_easy():
    response = mine_block("easy")
    return jsonify(response), 200

# Hard mode mining
@app.route('/mining/hard')
def mining_block_hard():
    response = mine_block("hard")
    return jsonify(response), 200

def mine_block(mode):
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if not is_valid:
        return {"error": "Mining failed. Blockchain is invalid", "is_valid": "false"}

    try:
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block["nonce"]
    except IndexError:
        return {"error": "Cannot mine a new block. Chain is empty."}

    BTC = 1  # Set the value of BTC
    blockchain.transaction = blockchain.transaction + BTC  # Add BTC to self.transaction

    if mode == "easy":
        nonce = blockchain.proof_of_work_easy(previous_nonce)
    elif mode == "hard":
        nonce = blockchain.proof_of_work_hard(previous_nonce)
    else:
        return {"error": "Invalid mining mode"}

    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(nonce, previous_hash)

    if block:
        response = {
            "message": f"Mining ({mode}) completed",
            "index": block["index"],
            "data": block["data"],
            "timestamp": block["timestamp"],
            "nonce": block["nonce"],
            "previous_hash": block["previous_hash"],
            "hash": blockchain.hash(block),  # Add hash to the response
            "is_valid": "true"
        }
        return response
    else:
        return {"message": "Block not created. No changes in data, nonce, or previous hash.", "is_valid": "false"}

@app.route('/is_valid')
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': "Blockchain is Valid"}
    else:
        response = {"message": "Have problem, Blockchain is Invalid"}
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
