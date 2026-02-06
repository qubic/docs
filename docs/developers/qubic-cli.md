---
title: Qubic CLI
---

# Qubic CLI

The Qubic CLI (Command Line Interface) is an essential tool for developers to communicate with Qubic nodes. It allows you to perform various operations like checking balances, sending transactions, and interacting with smart contracts.

## Installation

You can get the code and installation instructions from the [Qubic CLI GitHub repository](https://github.com/qubic/qubic-cli).


## Command Reference

Here are the essential CLI commands you'll need for development:

### Basic Commands

- `./qubic-cli -help`: Prints the help message with all available commands
- `./qubic-cli -nodeip <IPv4_ADDRESS>`: Specifies the IP address of the target node. You can find a list of computor IPs on the [Qubic Live Network page](https://app.qubic.li/network/live).
- `./qubic-cli -nodeport <PORT>`: Specifies the port of the target node. The default port is `21841`.

### Account Operations

- `./qubic-cli -getbalance <IDENTITY>`: Retrieves the balance of a specified identity
- `./qubic-cli -sendtoaddress <TARGET_IDENTITY> <AMOUNT>`: Sends Qubic to a target identity

### Node Information

- `./qubic-cli -getcurrenttick`: Fetches the current tick information of the node
- `./qubic-cli -gettxinfo <TX_ID>`: Gets transaction information

### Using Seeds

When working with test accounts, you can use a seed phrase to sign transactions:

```bash
./qubic-cli -nodeip YOUR_NODE_IP -nodeport YOUR_NODE_PORT -seed YOUR_SEED -somecommand
```

## Smart Contract Interaction

The CLI is particularly useful for testing smart contracts. For example, to interact with a deployed smart contract:

1. Get the current tick information:
   ```bash
   ./qubic-cli -nodeip YOUR_NODE_IP -nodeport YOUR_NODE_PORT -getcurrenttick
   ```

2. Call a smart contract function:
   ```bash
   ./qubic-cli -nodeip YOUR_NODE_IP -nodeport YOUR_NODE_PORT -seed YOUR_SEED -callcontract CONTRACT_INDEX FUNCTION_INDEX AMOUNT
   ```

For a complete list of commands, use the `-help` flag or visit the [Qubic CLI GitHub repository](https://github.com/qubic/qubic-cli).
