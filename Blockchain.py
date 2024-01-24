import datetime
import hashlib
import json
import time
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []  # List to store blocks
        self.transaction = 0
        self.create_block(nonce=1, previous_hash="0")

    def create_block(self, nonce, previous_hash):
        current_time = datetime.datetime.now()
        seconds_to_next_ten_minutes = (10 * 60 - (current_time.minute * 60 + current_time.second)) % (10 * 60)
        timestamp_in_future = current_time + datetime.timedelta(seconds=seconds_to_next_ten_minutes)

        block = {
            "index": len(self.chain) + 1,
            "data": self.transaction,
            "timestamp": str(timestamp_in_future.strftime("%Y-%m-%d %H:%M:%S")),
            "nonce": nonce,
            "previous_hash": previous_hash
        }
        self.chain.append(block)
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
        target_zeros = 6
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:target_zeros] == "0" * target_zeros:
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce

    def is_chain_valid(self, chain):
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

# สร้างอ็อบเจกต์ Blockchain
blockchain = Blockchain()

# กำหนดแอพ Flask
app = Flask(__name__)

# รายการที่มีการเรียกใช้งานในเว็บแอพ Flask
@app.route('/')
def hello():
    return "<p>Hello world<p/>"

@app.route('/get_chain')
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

# easy mode minning
@app.route('/mining/easy') 
def mining_block():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    BTC = 1
    blockchain.transaction = blockchain.transaction + BTC
    try:
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block["nonce"]
    except IndexError:
        return jsonify({"error": "Cannot mine a new block. Chain is empty."}), 400

    if is_valid:
        nonce = blockchain.proof_of_work_easy(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)

        response = {
            "message": "Mining เรียบร้อย",
            "index": block["index"],
            "data": block["data"],
            "timestamp": block["timestamp"],
            "nonce": block["nonce"],
            "previous_hash": block["previous_hash"],
            "isvalid": "true"
        }
    else:
        response = {
            "message": "mining failed block chain is invalid",
            "is_invalid": "false"
        }

    return jsonify(response), 200

# easy mode hard
@app.route('/mining/hard') 
def mining_block_hard():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    BTC = 1
    blockchain.transaction = blockchain.transaction + BTC
    try:
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block["nonce"]
    except IndexError:
        return jsonify({"error": "Cannot mine a new block. Chain is empty."}), 400

    if is_valid:
        nonce = blockchain.proof_of_work_hard(previous_nonce)  # เปลี่ยนเมธอดเป็น proof_of_work_hard
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)

        response = {
            "message": "Mining เรียบร้อย",
            "index": block["index"],
            "data": block["data"],
            "timestamp": block["timestamp"],
            "nonce": block["nonce"],
            "previous_hash": block["previous_hash"],
            "isvalid": "true"
        }
    else:
        response = {
            "message": "mining failed block chain is invalid",
            "is_invalid": "false"
        }

    return jsonify(response), 200

@app.route('/is_valid')
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': "Blockchain is Valid"}
    else:
        response = {"message": "Have problem , Blockchain is InValid"}
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
