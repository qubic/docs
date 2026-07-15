---
title: Frontend Integration
description: "Guide to building Qubic dApps: wallet integration, RPC communication, and smart contract interaction, with links to reference implementations."
---

# Building Frontend Applications for Qubic

This guide provides an overview of how to build frontend applications (dApps) for Qubic — covering wallet integration, RPC communication, and smart contract interaction — with links to complete reference implementations.

## Key Components of a Qubic dApp

A typical Qubic dApp consists of:
1. A frontend user interface
2. Wallet integration for transaction signing
3. RPC communication with Qubic nodes
4. Smart contract interaction logic

## Complete Frontend Example

The most comprehensive example of a Qubic frontend application can be found in the [HM25 Frontend Example repository](https://github.com/icyblob/hm25-frontend). This repository demonstrates:

- Complete wallet integrations (MetaMask Snap, WalletConnect, seed phrase, Vault file)
- Smart contract interaction patterns
- Transaction signing and broadcasting
- Real-time data fetching from Qubic nodes

We highly recommend exploring this codebase as a starting point for your application.

## Wallet Integration

Qubic supports multiple wallet integration options:

- **Qubic Wallet Extension** - Native dApp integration via the `window.qubic` provider API, exposed by the [Qubic Wallet browser extension](https://github.com/qubic/wallet-extension). See the [wallet-extension-dapp sample](https://github.com/qubic/wallet-extension-dapp) for a working integration.
- **WalletConnect support** - For connecting a dApp to the official [Qubic mobile wallet](https://github.com/qubic/wallet-app) (iOS/Android) via WalletConnect. See the [official WalletConnect integration guide](https://github.com/qubic/wallet-app/blob/main/walletconnect.md) and the [wallet-app-dapp sample](https://github.com/qubic/wallet-app-dapp) for a working integration.
- **MetaMask Snap integration** - For users who already use MetaMask. See the [Qubic MetaMask Snap](https://github.com/qubic/qubic-mm-snap), also available in the [MetaMask Snaps directory](https://snaps.metamask.io/snap/npm/qubic-lib/qubic-mm-snap/).
- **Seed phrase login** - For direct access with a seed phrase (not recommended)
- **Vault file authentication** - For secure stored identities (not recommended)

The MetaMask Snap, seed phrase, and Vault file options are all demonstrated in the [HM25 Frontend Example](https://github.com/icyblob/hm25-frontend).

## Connecting to Nodes

Your application will need to connect to a Qubic node via the RPC API:

- **Public mainnet node**: `https://rpc.qubic.org`
- **Custom node**: Your own deployed node (see [Qubic Node documentation](qubic-node.md))

The [Qubic TypeScript Library](https://github.com/qubic/ts-library) provides tools for connecting to nodes:

```javascript
import { QubicConnector } from 'qubic-ts-library/dist/qubicConnector'
const connector = new QubicConnector("https://rpc.qubic.org");
```

## Smart Contract Interaction Patterns

There are two main ways to interact with smart contracts:

1. **Reading data** (using functions)
   - Use the `/v1/querySmartContract` RPC endpoint
   - See the [HM25 Frontend HM25Api.jsx](https://github.com/icyblob/hm25-frontend/blob/main/src/components/api/HM25Api.jsx) for implementation

2. **Writing data** (using procedures)
   - Create, sign, and broadcast transactions
   - Target the contract with the appropriate function index and parameters
   - See the Echo and Burn function implementations in the HM25 Frontend example

For implementation details, explore:
- [`fetchHM25Stats`](https://github.com/icyblob/hm25-frontend/blob/main/src/components/api/HM25Api.jsx#L9) - Example of reading from a contract
- [`buildEchoTx`](https://github.com/icyblob/hm25-frontend/blob/main/src/components/api/HM25Api.jsx#L39) - Example of creating a transaction for a contract procedure

## Required Libraries

1. **Qubic TypeScript Library**
   ```bash
   yarn add @qubic-lib/qubic-ts-library
   ```

2. **Optional: Qubic Vault Library** (for vault file support)
   ```bash
   yarn add @qubic-lib/qubic-ts-vault-library
   ```

## Development Workflow

1. **Setup Project**: Create a React/Vue/Angular project
2. **Install Libraries**: Add the Qubic TypeScript Library
3. **Configure Node Connection**: Set up connector to testnet or custom node
4. **Implement Wallet Integration**: Use the patterns from HM25 Frontend
5. **Build Smart Contract Interface**: Create functions that read/write to your contract
6. **Develop UI Components**: Create forms, displays and interaction elements

## Next Steps

- Explore the [Qubic TypeScript Library documentation](library-typescript.md)
- Read the [RPC API documentation](../api/rpc) for all available endpoints
- Clone and study the [HM25 Frontend Example](https://github.com/icyblob/hm25-frontend)
- Check the [Smart Contract documentation](../learn/smart-contracts.md) to understand the backend 