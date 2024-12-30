async function main() {
  // Obtenha o contrato e as contas
  const [deployer] = await ethers.getSigners();
  console.log("Implantando contrato com a conta:", deployer.address);

  // Pegue o contrato LocalToken
  const Token = await ethers.getContractFactory("LocalToken");

  // Implemente o contrato
  const token = await Token.deploy();
  console.log("Contrato LocalToken implantado para:", token.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
