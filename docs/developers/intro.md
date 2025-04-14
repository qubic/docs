---
title: Become a developer
---

# Become a Developer

Welcome to Qubic development! This guide will help you navigate the available resources and direct you to the tools you need for your specific use case.

## Choose Your Path

### 1. Building Smart Contracts

If you want to create and deploy smart contracts on Qubic:

1. **Get Started with the Qubic Dev Kit**
   - The [Qubic Dev Kit](https://github.com/qubic/qubic-dev-kit) provides everything you need to set up a testnet node and deploy smart contracts
   - It includes the HM25 template smart contract with example features like Echo and Burn
   - Check our [Dev Kit docs](dev-kit.md) for a quick overview

2. **Understand Smart Contract Structure**
   - Smart contracts in Qubic are written in C++ using the [Qubic Programming Interface (QPI)](qpi.md)
   - Fork the [Qubic Core repository](https://github.com/qubic/core) and check the existing contracts in `src/contracts`

3. **Test and Deploy**
   - Use the [Qubic CLI](https://github.com/qubic/qubic-cli) to interact with your smart contract
   - Access testnet resources from our [Testnet Resources](testnet-resources.md) page

### 2. Building Frontend Applications

If you want to build applications that interact with the Qubic network:

1. **Connect to Qubic Nodes**
   - Use our [RPC endpoints](../api/rpc.md) to connect to public nodes or set up your own
   - The main testnet endpoint is available at `https://testnet-rpc.qubic.org`

2. **Integrate Wallet Solutions**
   - For complete wallet integration examples (MetaMask Snap, WalletConnect, Seed phrases, Vault files), check out the [HM25 Frontend Example](https://github.com/icyblob/hm25-frontend)
   - This repository demonstrates all key wallet connection methods

3. **Use the TypeScript Library**
   - The [Qubic TypeScript Library](https://github.com/qubic/ts-library) provides tools for creating transactions and interacting with the network
   - See our [TypeScript Library docs](library-typescript.md) for installation instructions

### 3. Smart Contract Interaction

To interact with existing smart contracts:

1. **Learn Contract Interaction Basics**
   - Check our [Frontend Integration](frontend-integration.md) guide for an overview
   - The [HM25 Frontend Example](https://github.com/icyblob/hm25-frontend) contains complete implementation examples

2. **Understand Data Structures**
   - Smart contracts use specific input/output structures defined in their code
   - Find example code in the [HM25 Template](https://github.com/qubic/core/blob/madrid-2025/src/contracts/HM25.h)

## Quick Reference Links

- **Set up development environment**: [Qubic Dev Kit](https://github.com/qubic/qubic-dev-kit)
- **Core implementation**: [Qubic Core](https://github.com/qubic/core)
- **Command line interaction**: [Qubic CLI](https://github.com/qubic/qubic-cli)
- **TypeScript development**: [Qubic TypeScript Library](https://github.com/qubic/ts-library)
- **Wallet management**: [Qubic Vault TypeScript Library](https://github.com/qubic/ts-vault-library)
- **Frontend example**: [HM25 Frontend](https://github.com/icyblob/hm25-frontend)
- **Online CLI interface**: [QubicDev.com](https://qubicdev.com)

## Getting Help

- Join the [Qubic Discord](https://discord.gg/qubic) community for support and collaboration
- Check for available [Qubic Grants](grants.md) to fund your project