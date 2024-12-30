require("@nomiclabs/hardhat-ethers");

module.exports = {
  solidity: "0.8.0",
  networks: {
    hardhat: {
      chainId: 1337, // ID da rede local
    },
    localhost: {
      url: "http://127.0.0.1:8545", // URL da rede local
      accounts: ["<PRIVATE_KEY>"] // A chave privada para a carteira do desenvolvedor
    }
  }
};
