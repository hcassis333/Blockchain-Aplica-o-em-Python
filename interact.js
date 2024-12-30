async function interact() {
  const [deployer] = await ethers.getSigners();
  const tokenAddress = "<CONTRACT_ADDRESS>"; // Endereço do contrato implantado
  const Token = await ethers.getContractAt("LocalToken", tokenAddress);

  // Chame uma função do contrato (exemplo: mint)
  const tx = await Token.mint(deployer.address, ethers.utils.parseUnits("100", 18)); // Mint 100 tokens
  await tx.wait();

  console.log("100 tokens minerados!");
}

interact();
