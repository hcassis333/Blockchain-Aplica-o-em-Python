const Web3 = require('web3');
const web3 = new Web3('http://127.0.0.1:8545');

// Exemplo: Pegar o último bloco
async function getLatestBlock() {
  const latestBlock = await web3.eth.getBlock('latest');
  console.log(latestBlock);
}

getLatestBlock();
