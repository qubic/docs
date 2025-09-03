---
title: Qubic Dev Kit
---

# Qubic Dev Kit

The [Qubic Dev Kit](https://github.com/qubic/qubic-dev-kit) is your go-to tool for setting up a Qubic testnet node and running the HM25 Smart Contract demo for Hackathon Madrid 2025. It streamlines the process for developers looking to create and test their own smart contracts.

## Important Notes

- **Dev Kit Requirements**: Essential for developing and testing smart contracts, simulating the entire Qubic blockchain in a single environment. If you only need to interact with existing contracts, consider using the RPC API and wallet solutions instead.

- **Support and Resources**: For any questions or if you need a server setup, please reach out in the #dev channel on our Discord. We may be able to provide server resources and assistance.

## Overview

The Dev Kit manages:
- Complete Qubic development environment setup
- EFI file building
- Testnet node deployment with your smart contract
- RPC access for testing

## Development Environment Setup

To set up the environment for developing QUBIC smart contracts, you need two main components: `Visual Studio` and the [`Qubic Core`](https://github.com/qubic/core) repository.

:::info
We recommend using [Qubic Core Lite](smart-contracts/resources/qubic-lite-core.md) repo instead of the official Qubic Core so you can build and run the local testnet with your smart contract **directly in OS** without using a VM.
:::

### 1. Install Visual Studio

1. Go to [https://visualstudio.microsoft.com/](https://visualstudio.microsoft.com/) and download Visual Studio
2. Open the Visual Studio Installer and select the `Desktop development with C++` workload
3. Complete the installation process

### 2. Clone and Setup the Repository

1. Choose `Clone a repository` in Visual Studio
2. Paste the URL: `https://github.com/qubic/core.git`
3. Once cloned, open `Qubic.sln` from the solution explorer
4. Test your setup by right-clicking the `test` project and selecting `Build`

If you see successful build logs, congratulations! Your development environment is ready.

## Getting Started with Dev Kit

For complete documentation and setup instructions, check out the Dev Kit on GitHub: [Qubic Dev Kit](https://github.com/qubic/qubic-dev-kit)

The Dev Kit provides a streamlined workflow for:
- Setting up a complete development environment
- Building and testing smart contracts locally
- Deploying to testnet for integration testing

## Key Features

- **Optimized for Demo Branch**: The Dev Kit works with the `madrid-2025` branch of the Qubic core repository
- **Built-in Smart Contract Template**: Includes the HM25 template smart contract with Echo and Burn functions
- **One-Command Deployment**: Deploy a complete node with your smart contract using a single command
- **Local Testing Environment**: Run a complete Qubic testnet locally for development and testing

## Next Steps

After setting up your environment:

1. **Learn Smart Contract Structure**: Check out our [Smart Contract Overview](smart-contracts/overview.md)
2. **Follow the Getting Started Guide**: Complete the [Getting Started Tutorial](smart-contracts/getting-started/setup-enviroment.md)
3. **Understand QPI**: Read about the [Qubic Programming Interface](qpi.md)
4. **Explore Examples**: Look at [Smart Contract Examples](smart-contracts/sc-by-examples/assets-and-shares.md)

