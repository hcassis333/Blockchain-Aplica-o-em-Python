import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import hashlib
import time
import os
from datetime import datetime
from typing import List, Dict

# Classes Block e Blockchain do código anterior permanecem iguais
[Todas as classes anteriores...]

class BlockchainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Manager")
        self.root.geometry("800x600")
        self.blockchain = Blockchain(difficulty=4)
        
        # Configurar o estilo
        style = ttk.Style()
        style.configure("TNotebook", padding=10)
        
        # Criar notebook para abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Criar as diferentes abas
        self.create_transactions_tab()
        self.create_mining_tab()
        self.create_blockchain_view_tab()
        self.create_balance_tab()
        
    def create_transactions_tab(self):
        transactions_frame = ttk.Frame(self.notebook)
        self.notebook.add(transactions_frame, text='Transações')
        
        # Campos de entrada
        ttk.Label(transactions_frame, text="Remetente:").pack(pady=5)
        self.sender_entry = ttk.Entry(transactions_frame, width=50)
        self.sender_entry.pack(pady=5)
        
        ttk.Label(transactions_frame, text="Destinatário:").pack(pady=5)
        self.recipient_entry = ttk.Entry(transactions_frame, width=50)
        self.recipient_entry.pack(pady=5)
        
        ttk.Label(transactions_frame, text="Quantidade:").pack(pady=5)
        self.amount_entry = ttk.Entry(transactions_frame, width=50)
        self.amount_entry.pack(pady=5)
        
        # Botão de adicionar transação
        ttk.Button(transactions_frame, 
                  text="Adicionar Transação", 
                  command=self.add_transaction).pack(pady=20)
        
        # Lista de transações pendentes
        ttk.Label(transactions_frame, text="Transações Pendentes:").pack(pady=5)
        self.pending_tx_text = scrolledtext.ScrolledText(transactions_frame, 
                                                       width=70, 
                                                       height=15)
        self.pending_tx_text.pack(pady=5)
        
    def create_mining_tab(self):
        mining_frame = ttk.Frame(self.notebook)
        self.notebook.add(mining_frame, text='Mineração')
        
        ttk.Label(mining_frame, text="Endereço do Minerador:").pack(pady=5)
        self.miner_entry = ttk.Entry(mining_frame, width=50)
        self.miner_entry.pack(pady=5)
        
        ttk.Button(mining_frame, 
                  text="Minerar Bloco", 
                  command=self.mine_block).pack(pady=20)
        
        self.mining_status = ttk.Label(mining_frame, text="")
        self.mining_status.pack(pady=5)
        
    def create_blockchain_view_tab(self):
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text='Ver Blockchain')
        
        self.chain_text = scrolledtext.ScrolledText(view_frame, 
                                                  width=70, 
                                                  height=30)
        self.chain_text.pack(pady=10)
        
        ttk.Button(view_frame, 
                  text="Atualizar Visualização", 
                  command=self.update_chain_view).pack(pady=5)
        
    def create_balance_tab(self):
        balance_frame = ttk.Frame(self.notebook)
        self.notebook.add(balance_frame, text='Consultar Saldo')
        
        ttk.Label(balance_frame, text="Endereço:").pack(pady=5)
        self.balance_entry = ttk.Entry(balance_frame, width=50)
        self.balance_entry.pack(pady=5)
        
        ttk.Button(balance_frame, 
                  text="Verificar Saldo", 
                  command=self.check_balance).pack(pady=20)
        
        self.balance_label = ttk.Label(balance_frame, text="")
        self.balance_label.pack(pady=5)
        
    def add_transaction(self):
        try:
            sender = self.sender_entry.get()
            recipient = self.recipient_entry.get()
            amount = float(self.amount_entry.get())
            
            if not all([sender, recipient, amount]):
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
                
            self.blockchain.add_transaction(sender, recipient, amount)
            self.update_pending_transactions()
            messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
            
            # Limpar campos
            self.sender_entry.delete(0, tk.END)
            self.recipient_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
            
    def mine_block(self):
        miner = self.miner_entry.get()
        if not miner:
            messagebox.showerror("Erro", "Digite o endereço do minerador!")
            return
            
        self.mining_status.config(text="Minerando...")
        self.root.update()
        
        self.blockchain.mine_pending_transactions(miner)
        self.blockchain.save_chain()
        
        self.mining_status.config(text="Bloco minerado com sucesso!")
        self.update_chain_view()
        self.update_pending_transactions()
        
    def check_balance(self):
        address = self.balance_entry.get()
        if not address:
            messagebox.showerror("Erro", "Digite um endereço!")
            return
            
        balance = self.blockchain.get_balance(address)
        self.balance_label.config(text=f"Saldo: {balance}")
        
    def update_chain_view(self):
        self.chain_text.delete(1.0, tk.END)
        
        for block in self.blockchain.chain:
            self.chain_text.insert(tk.END, f"\nBloco #{block.index}\n")
            self.chain_text.insert(tk.END, f"Timestamp: {datetime.fromtimestamp(block.timestamp)}\n")
            self.chain_text.insert(tk.END, f"Hash: {block.hash}\n")
            self.chain_text.insert(tk.END, f"Hash anterior: {block.previous_hash}\n")
            self.chain_text.insert(tk.END, f"Nonce: {block.nonce}\n")
            self.chain_text.insert(tk.END, "Transações:\n")
            
            for tx in block.transactions:
                self.chain_text.insert(tk.END, 
                    f"  De: {tx['from']} Para: {tx['to']} Valor: {tx['amount']}\n")
            
            self.chain_text.insert(tk.END, "-" * 50 + "\n")
            
    def update_pending_transactions(self):
        self.pending_tx_text.delete(1.0, tk.END)
        
        for tx in self.blockchain.pending_transactions:
            self.pending_tx_text.insert(tk.END, 
                f"De: {tx['from']} Para: {tx['to']} Valor: {tx['amount']}\n")

def main():
    root = tk.Tk()
    app = BlockchainGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()