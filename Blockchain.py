import datetime
import hashlib
import json
from flask import Flask, jsonify


class Blockchain:
    def __init__(self):
        self.chain = []  # List to store blocks
        self.transaction = 0 
        self.create_block(nonce=1, previous_hash="0")

    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "data" :self.transaction,
            "timestamp": str(datetime.datetime.now()),
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

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_proof = False

        while not check_proof:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_nonce += 1
        return new_nonce
    #ตรวจสอบ block 
    def is_chain_valid(self,chain):
        previous_block= chain[0]
        block_index = 1 
        while block_index<len(chain):
            block = chain[block_index] #กำหนล่องที่ตรวจสอบ
            if block["previous_hash"] != self.hash(previous_block):
                return False 
            
            previous_nonce = previous_block["nonce"]
            nonce = block["nonce"]
            hashoperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()

            if hashoperation[:4]!="0000":
                return False
             
            previous_block = block=block
            block_index+=1

        return True



blockchain = Blockchain()
app = Flask(__name__)

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

@app.route('/mining')
def mining_block():

    BTC = 1
    blockchain.transaction = blockchain.transaction+BTC
    try:
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block["nonce"]
    except IndexError:
        return jsonify({"error": "Cannot mine a new block. Chain is empty."}), 400

    nonce = blockchain.proof_of_work(previous_nonce)

    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(nonce, previous_hash)

    response = {
        "message": "Mining เรียบร้อย",
        "index": block["index"],
        "data":block["data"],
        "timestamp": block["timestamp"],
        "nonce": block["nonce"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200


@app.route('/is_valid')
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = { 'message':"Blockchain is Valid"}
    else :
        response = {"message":"Have problem , Blockchain is InValid"}
    return jsonify(response), 200



if __name__ == "__main__":
    app.run()
