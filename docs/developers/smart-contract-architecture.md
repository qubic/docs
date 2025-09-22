---
title: Smart Contract Architecture
---

# Smart Contract Architecture

## Open Source and Transparent

**Public availability**: All contracts are available in the official repository

One of Qubic's most significant advantages is complete transparency. Unlike many blockchain platforms where smart contracts are deployed as compiled bytecode that's difficult to audit, Qubic takes a radically different approach.

- **Location**: https://github.com/qubic/core/tree/main/src/contracts
- **Complete source code**: Every smart contract running on Qubic mainnet has its full C++ source code publicly available in the official repository
- **No hidden logic**: There are no proprietary contracts or closed-source components. What you see in the repository is exactly what's running on the network
- **Community auditing**: The open-source nature enables the entire community to review, audit, and understand the behavior of all contracts
- **Version control**: The git history shows how contracts have evolved over time, providing transparency about changes and updates

**Technical implementation**:

- **C++ implementation**: Smart contracts are written in C++ and compiled to native machine code, not bytecode
- **Direct execution on UEFI ("bare metal")**: Contracts run directly on the Computor hardware through the UEFI layer, without any virtual machine, which is why Qubic achieves such exceptional performance.
- **Deterministic compilation**: The same source code always produces identical executable contracts, ensuring reproducible deployments
- **No runtime interpretation**: Unlike Ethereum's EVM or other VM-based systems, there's no runtime interpretation overhead

## Contract Identification System

**Deterministic identification**: Each smart contract is assigned a numerical index, from which its unique public key identifier is derived in a deterministic way.

All smart contracts in Qubic use a dual identification system for deterministic addressing and transaction targeting. Each contract has:

1. **Hardcoded numerical index** - Used for contract registration and internal referencing
2. **Public key identifier** - 60-character string used for targeting transactions

### Contract Indices and Identifiers

```json
{
  "QX": {
    "index": 1,
    "id": "BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARMID"
  },
  "QUOTTERY": {
    "index": 2,
    "id": "CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNKL"
  },
  "RANDOM": {
    "index": 3,
    "id": "DAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANMIG"
  },
  "QUTIL": {
    "index": 4,
    "id": "EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVWRF"
  },
  "MLM": {
    "index": 5,
    "id": "FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYWJB"
  },
  "GQMPROP": {
    "index": 6,
    "id": "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQGNM"
  },
  "SWATCH": {
    "index": 7,
    "id": "HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYCM"
  },
  "CCF": {
    "index": 8,
    "id": "IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABXSH"
  },
  "QEARN": {
    "index": 9,
    "id": "JAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVKHO"
  },
  "QVAULT": {
    "index": 10,
    "id": "KAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAXIUO"
  },
  "MSVAULT": {
    "index": 11,
    "id": "LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKPTJ"
  },
  "QBAY": {
    "index": 12,
    "id": "MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWLWD"
  }
}
```

**Usage contexts**:

- **Contract Index**: Used in RPC calls like `querySmartContract` to specify which contract to interact with
- **Public Key ID**: Used as the `destination` field in transactions when calling contract procedures

**Additional resources**:

- **Contract discovery and specifications**: https://qforge.qubicdev.com/
- **Contract and token explorer**: https://explorer.qubic.org/network/assets/smart-contracts

The explorer provides comprehensive information about all contracts and tokens deployed on the Qubic network, including their current state, transaction history, and interaction details.

## Functions vs Procedures - Separation of Concerns

### Functions (Read-Only)

```cpp
// Example from QX contract
struct Fees_output {
    uint32 assetIssuanceFee;
    uint32 transferFee;
    uint32 tradeFee;
};

PUBLIC_FUNCTION(Fees) {
    output.assetIssuanceFee = state._assetIssuanceFee;
    output.transferFee = state._transferFee;
    output.tradeFee = state._tradeFee;
}
```

**Characteristics**:

- **Immutable**: Cannot modify contract state
- **No cost**: Don't require transactions, only RPC queries
- **Deterministic**: Always return the same result for the same state

### Procedures (Write Operations)

```cpp
// Example from QX contract
struct AddToBidOrder_input {
    id issuer;
    uint64 assetName;
    sint64 price;
    sint64 numberOfShares;
};

PUBLIC_PROCEDURE(AddToBidOrder) {
    // Validations and business logic
    if (qpi.invocationReward() < smul(input.price, input.numberOfShares)) {
        // Error handling
        return;
    }

    // State modification
    state._assetOrders.add(/* ... */);
    state._entityOrders.add(/* ... */);
}
```

**Characteristics**:

- **Mutable**: Can modify contract state
- **Require transactions**: Must be invoked through signed transactions
- **Potentially costly**: May require QUs depending on contract logic

## Registration and Indexing System

```cpp
// Mapping functions to numeric indices
REGISTER_USER_FUNCTIONS_AND_PROCEDURES() {
    // Functions (queries)
    REGISTER_USER_FUNCTION(Fees, 1);                    // inputType = 1
    REGISTER_USER_FUNCTION(AssetAskOrders, 2);          // inputType = 2
    REGISTER_USER_FUNCTION(AssetBidOrders, 3);          // inputType = 3
    REGISTER_USER_FUNCTION(EntityAskOrders, 4);         // inputType = 4

    // Procedures (transactions)
    REGISTER_USER_PROCEDURE(IssueAsset, 1);             // inputType = 1
    REGISTER_USER_PROCEDURE(AddToAskOrder, 5);          // inputType = 5
    REGISTER_USER_PROCEDURE(AddToBidOrder, 6);          // inputType = 6
    REGISTER_USER_PROCEDURE(RemoveFromAskOrder, 7);     // inputType = 7
}
```

**Registration importance**:

- **Unique identification**: Each function/procedure has a specific numeric index
- **Public interface**: Defines the contract's available API
- **Validation**: Only registered functions can be invoked externally
