from flask import Flask, render_template, request, jsonify
import hashlib
import time
import json
import os
from datetime import datetime
from typing import List, Dict

class Block:
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def to_dict(self):
        return {
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    @classmethod
    def from_dict(cls, block_dict):
        block = cls(
            block_dict['index'],
            block_dict['transactions'],
            block_dict['timestamp'],
            block_dict['previous_hash'],
            block_dict['nonce']
        )
        block.hash = block_dict['hash']
        return block

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10
        
        if os.path.exists('blockchain.json'):
            self.load_chain()
        else:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)
        self.save_chain()
    
    def save_chain(self):
        chain_data = {
            'chain': [block.to_dict() for block in self.chain],
            'pending_transactions': self.pending_transactions,
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward
        }
        with open('blockchain.json', 'w') as f:
            json.dump(chain_data, f, indent=2)
    
    def load_chain(self):
        with open('blockchain.json', 'r') as f:
            data = json.load(f)
            self.chain = [Block.from_dict(block_dict) for block_dict in data['chain']]
            self.pending_transactions = data['pending_transactions']
            self.difficulty = data['difficulty']
            self.mining_reward = data['mining_reward']

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address: str):
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )
        
        block = self.proof_of_work(block)
        self.chain.append(block)
        self.pending_transactions = [
            {"from": "network", "to": miner_address, "amount": self.mining_reward}
        ]
        self.save_chain()
        return block

    def proof_of_work(self, block: Block) -> Block:
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block

    def add_transaction(self, sender: str, recipient: str, amount: float):
        self.pending_transactions.append({
            "from": sender,
            "to": recipient,
            "amount": amount
        })
        self.save_chain()

    def get_balance(self, address: str) -> float:
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["from"] == address:
                    balance -= transaction["amount"]
                if transaction["to"] == address:
                    balance += transaction["amount"]
        return balance

    def get_chain_data(self):
        return {
            'chain': [block.to_dict() for block in self.chain],
            'pending_transactions': self.pending_transactions
        }

# Inicializar Flask e Blockchain
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.get_chain_data())

@app.route('/api/transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()
    try:
        blockchain.add_transaction(
            data['sender'],
            data['recipient'],
            float(data['amount'])
        )
        return jsonify({'message': 'Transação adicionada com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/mine', methods=['POST'])
def mine():
    data = request.get_json()
    try:
        block = blockchain.mine_pending_transactions(data['miner'])
        return jsonify({
            'message': 'Novo bloco minerado!',
            'block': block.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/balance/<address>')
def get_balance(address):
    try:
        balance = blockchain.get_balance(address)
        return jsonify({'balance': balance})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)