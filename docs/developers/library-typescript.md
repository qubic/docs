---
title: Typescript Libraries
---

# Typescript Libraries

## Qubic TypeScript Library

The [Qubic TypeScript Library](https://github.com/qubic/ts-library) provides everything needed to interact with the Qubic network from JavaScript/TypeScript applications.

### Installation

```bash
yarn add @qubic-lib/qubic-ts-library
# or
npm install @qubic-lib/qubic-ts-library
```

### Basic Usage

```typescript
// Import helper
import { QubicHelper } from 'qubic-ts-library/dist/qubicHelper'
import { QubicConnector } from 'qubic-ts-library/dist/qubicConnector'

// Create helper instance
const helper = new QubicHelper();

// Create an ID Package from seed phrase
const id = await helper.createIdPackage("your-seed-phrase");

// Connect to a node
const connector = new QubicConnector("https://rpc.qubic.org");

// Get balance
const balance = await connector.getBalance(id.publicId);
```

### Key Features

- Creating and managing identities
- Connecting to Qubic nodes
- Fetching balances
- Creating and signing transactions
- Smart contract interaction

For complete documentation and examples, visit:
- [GitHub Repository](https://github.com/qubic/ts-library)
- [Example Application](https://github.com/icyblob/hm25-frontend)

## Vault TypeScript Library

The [Qubic Vault TypeScript Library](https://github.com/qubic/ts-vault-library) provides tools for managing encrypted identity storage.

### Installation

```bash
yarn add @qubic-lib/qubic-ts-vault-library
# or
npm install @qubic-lib/qubic-ts-vault-library
```

### Basic Usage

```typescript
import { QubicVault } from 'qubic-ts-vault-library/dist/qubicVault'

// Create a new vault with password
const vault = new QubicVault();
vault.createVault("secure-password");

// Add an identity to the vault
vault.addIdentity("identity-name", "seed-phrase");

// Export and save
const vaultData = vault.exportVault();
// Now save vaultData to file system
```

For complete vault library documentation, visit the [GitHub Repository](https://github.com/qubic/ts-vault-library).
