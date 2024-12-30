from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Blockchain e dados da blockchain
blockchain = {
    "chain": [],
    "pending_transactions": []
}

# Funções auxiliares para persistência
def load_wallets():
    try:
        with open("wallets.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_wallets():
    with open("wallets.json", "w") as file:
        json.dump(wallets, file, indent=4)

# Carregar carteiras
wallets = load_wallets()

# Inicializar carteiras se o arquivo estiver vazio
if not wallets:
    wallets = {
        "0x1234567890abcdef": {"balance": 100},  # Carteira 1
        "0xabcdef1234567890": {"balance": 200}   # Carteira 2
    }
    save_wallets()

# Atualizar saldos
def update_balances(sender, recipient, amount):
    if sender in wallets and wallets[sender]["balance"] >= amount:
        wallets[sender]["balance"] -= amount
        if recipient in wallets:
            wallets[recipient]["balance"] += amount
        else:
            wallets[recipient] = {"balance": amount}
        return True
    return False

# Rota para adicionar uma transação
@app.route('/api/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")

    if not sender or not recipient or not amount:
        return jsonify({"error": "Dados inválidos!"}), 400

    if update_balances(sender, recipient, amount):
        blockchain["pending_transactions"].append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        save_wallets()  # Salvar os saldos atualizados
        return jsonify({"message": "Transação criada com sucesso!"}), 200
    else:
        return jsonify({"error": "Saldo insuficiente ou endereço inválido!"}), 400

# Rota para consultar o saldo de uma carteira
@app.route('/api/balance/<address>', methods=['GET'])
def get_balance(address):
    if address in wallets:
        return jsonify({"address": address, "balance": wallets[address]["balance"]}), 200
    return jsonify({"error": "Endereço não encontrado!"}), 404

# Rota para exibir a blockchain
@app.route('/api/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain), 200

# Finalizar o servidor e salvar os dados das carteiras
import atexit
atexit.register(save_wallets)

# Inicializar o servidor
if __name__ == '__main__':
    app.run(port=5000)

@app.route('/')
def index():
    return "<h1>Bem-vindo à Blockchain Interface!</h1><p>Use as rotas da API para interagir com a blockchain.</p>"

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


tx = contract.functions.transfer("/0x1234567890abcdef", 100).transact()
web3.eth.wait_for_transaction_receipt(tx)
print(f"Novo saldo: {contract.functions.balanceOf('/0x1234567890abcdef').call()}")