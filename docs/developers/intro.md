---
title: Become a developer
---

# Become a Developer

Welcome to Qubic development! This guide will help you navigate the available resources and direct you to the tools you need for your specific use case.

## Choose Your Path

### 1. Building Smart Contracts

If you want to create and deploy smart contracts on Qubic:

1. **Start with the Overview**
   - Read our comprehensive [Smart Contracts Overview](smart-contracts/overview.md) to understand Qubic's unique baremetal execution model
   - Learn about IPO-based deployment and the advantages of running contracts without VMs or gas fees

2. **Set Up Your Environment**
   - **Recommended:** [AIO Qubic Dev Kit](smart-contracts/getting-started/setup-environment.md#aio-qubic-dev-kit-linux--recommended) — Linux, Docker-based, one repo with Core + Faucet + Wallet + RPC bundled. Fastest path to a working local environment.
   - Alternate (Windows/IDE): [Visual Studio + Qubic Core](smart-contracts/getting-started/setup-environment.md#visual-studio-windows--alternate).
   - Then walk through the full [Getting Started tutorial](smart-contracts/getting-started/setup-environment.md).

3. **Learn Contract Development**
   - Master the [Qubic Programming Interface (QPI)](qpi.md) - your complete guide to contract APIs
   - Understand [Contract Structure](smart-contracts/smart-contract/contract-structure.md) and [Data Types](smart-contracts/smart-contract/data-types.md)
   - Explore [Procedures and Functions](smart-contracts/smart-contract/procedures-and-functions.md)

4. **Practice with Examples**
   - Study [Assets and Shares Examples](smart-contracts/sc-by-examples/assets-and-shares.md)
   - Try the [QNS (Qubic Name Service) Example](smart-contracts/sc-by-examples/qns.md)

5. **Test and Deploy**
   - Use our [CLI Tools](smart-contracts/cli/Overview.md) for contract interaction
   - Follow [Testing Guidelines](smart-contracts/testing/overview.md) and access [Testnet Resources](testnet-resources.md)

### 2. Building Frontend Applications

If you want to build applications that interact with the Qubic network:

1. **Connect to Qubic Nodes**
   - Use our [RPC endpoints](../api/rpc.md) to connect to public nodes or set up your own
   - Follow the [RPC Setup Guide](smart-contracts/rpc/setup-rpc.md) for detailed configuration

2. **Integrate Wallet Solutions**
   - For complete wallet integration examples (MetaMask Snap, WalletConnect, Seed phrases, Vault files), check out the [HM25 Frontend Example](https://github.com/icyblob/hm25-frontend)
   - This repository demonstrates all key wallet connection methods

3. **Use a TypeScript Library**
   - [qubic-typescript](https://github.com/qubic/qubic-typescript) is the SDK to start with — transactions, RPC, live node subscriptions, typed contracts, and `@qubic.org/react` hooks, split into packages you install as needed (public beta)
   - [ts-library](https://github.com/qubic/ts-library) is the older single-package library. Use it if you're maintaining a project built on it, or need the raw node protocol from a browser
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
- **TypeScript development**: [qubic-typescript SDK](https://github.com/qubic/qubic-typescript) or [Qubic TypeScript Library](https://github.com/qubic/ts-library)
- **.NET development**: [Qubic.NET](https://github.com/qubic/Qubic.NET)
- **Wallet management**: [Qubic Vault TypeScript Library](https://github.com/qubic/ts-vault-library)
- **Frontend example**: [HM25 Frontend](https://github.com/icyblob/hm25-frontend)

## Getting Help

- Join the [Qubic Discord](https://join.qubic.org/discord) community for support and collaboration
- Check for available [Qubic Grants](grants.md) to fund your project