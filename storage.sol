// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BasicToken {
    string public name = "Violin";
    string public symbol = "VIOLIN";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    address public owner;

    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(uint256 _initialSupply) {
        owner = msg.sender; // Define o criador do contrato como o proprietário
        totalSupply = _initialSupply * 10 ** uint256(decimals); // Define o total de moedas
        balances[owner] = totalSupply; // O criador recebe todas as moedas no início
    }

    // Transferência direta
    function transfer(address _to, uint256 _value) public returns (bool) {
        require(balances[msg.sender] >= _value, "Saldo insuficiente.");
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // Aprovar terceiros para gastar
    function approve(address _spender, uint256 _value) public returns (bool) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    // Transferência por terceiros
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        require(balances[_from] >= _value, "Saldo insuficiente.");
        require(allowance[_from][msg.sender] >= _value, "Sem permissao para transferir.");
        balances[_from] -= _value;
        balances[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
}
