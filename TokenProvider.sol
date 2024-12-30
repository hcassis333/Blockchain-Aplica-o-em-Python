// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract LocalToken is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 1000000 * 10 ** 18;

    // Construtor agora passa o endereço do criador para o Ownable e parâmetros para ERC20
    constructor() ERC20("LocalToken", "LTK") {
        transferOwnership(msg.sender); // Definindo o dono do contrato como o endereço que o implantou
        _mint(msg.sender, 1000 * 10 ** 18); // Mint inicial para o criador do contrato
    }

    // Função para minerar tokens
    function mint(address to, uint256 amount) external onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "Excede o limite maximo de emissao");
        _mint(to, amount);
    }
}
