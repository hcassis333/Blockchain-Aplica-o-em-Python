import React, { useState, useEffect } from 'react';
import ProposalList from './components/ProposalList';
import WalletConnect from './components/WalletConnect';
import DAO_ABI from './abi/DAO_ABI.json';
import { ethers } from 'ethers';
import './styles/App.css';

const DAO_CONTRACT_ADDRESS = '0xSeuContratoAqui'; // Substitua pelo endereço do contrato

const App = () => {
  const [provider, setProvider] = useState(null);
  const [proposals, setProposals] = useState([]);
  const [isMetaMaskInstalled, setIsMetaMaskInstalled] = useState(false);

  // Detecta se o MetaMask está instalado
  useEffect(() => {
    if (typeof window.ethereum !== 'undefined') {
      setIsMetaMaskInstalled(true);
      console.log('MetaMask está instalado');
    } else {
      setIsMetaMaskInstalled(false);
      console.log('MetaMask não está instalado');
    }
  }, []);

  // Conectar à carteira MetaMask
  const handleWalletConnect = async () => {
    if (!isMetaMaskInstalled) {
      alert('Por favor, instale o MetaMask!');
      return;
    }

    try {
      const ethereum = window.ethereum;

      // Solicita a conexão da conta MetaMask
      const accounts = await ethereum.request({ method: 'eth_requestAccounts' });

      // Cria o provedor usando o MetaMask
      const connectedProvider = new ethers.providers.Web3Provider(ethereum);
      setProvider(connectedProvider);

      console.log('Conta conectada:', accounts[0]);
    } catch (error) {
      console.error('Erro ao conectar ao MetaMask:', error);
      alert('Erro ao conectar sua carteira');
    }
  };

  // Buscar propostas do contrato
  const fetchProposals = async () => {
    if (!provider) return;

    try {
      const signer = provider.getSigner();
      const contract = new ethers.Contract(DAO_CONTRACT_ADDRESS, DAO_ABI, signer);
      const data = await contract.getProposals();
      setProposals(data);
    } catch (error) {
      console.error('Erro ao buscar propostas:', error);
    }
  };

  // Votar em uma proposta
  const handleVote = async (proposalId, voteType) => {
    if (!provider) {
      alert('Conecte sua carteira primeiro!');
      return;
    }

    try {
      const signer = provider.getSigner();
      const contract = new ethers.Contract(DAO_CONTRACT_ADDRESS, DAO_ABI, signer);
      const tx = await contract.vote(proposalId, voteType);
      await tx.wait();
      alert('Voto registrado com sucesso!');
      fetchProposals(); // Atualizar propostas após votar
    } catch (error) {
      console.error('Erro ao votar:', error);
      alert('Erro ao registrar seu voto.');
    }
  };

  // Buscar propostas ao carregar o app ou ao conectar carteira
  useEffect(() => {
    if (provider) {
      fetchProposals();
    }
  }, [provider]);

  return (
    <div className="container">
      <h1>Sistema de Votação DAO</h1>
      <div>
        {isMetaMaskInstalled ? (
          <button onClick={handleWalletConnect}>Conectar à MetaMask</button>
        ) : (
          <p>MetaMask não está instalado. Por favor, instale a extensão MetaMask no seu navegador.</p>
        )}
      </div>
      <WalletConnect onConnect={handleWalletConnect} />
      <ProposalList proposals={proposals} onVote={handleVote} />
    </div>
  );
};

export default App;
