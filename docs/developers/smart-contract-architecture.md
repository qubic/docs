---
title: Smart Contract Architecture
---

# Smart Contract Architecture

## Open Source and Transparent

One of Qubic's most significant advantages is complete transparency. Unlike many blockchain platforms where smart contracts are deployed as compiled bytecode that's difficult to audit, Qubic takes a radically different approach: every smart contract running on Qubic mainnet has its full C++ source code publicly available.

**Source code**: https://github.com/qubic/core/tree/main/src/contracts

- **No hidden logic**: There are no proprietary contracts or closed-source components. What you see in the repository is exactly what's running on the network
- **Community auditing**: The open-source nature enables the entire community to review, audit, and understand the behavior of all contracts. To report vulnerabilities, see the [Qubic Vulnerability Evaluation process](https://github.com/qubic/qct/tree/main/qve)
- **Version control**: The git history shows how contracts have evolved over time, providing transparency about changes and updates

## Technical Implementation

- **C++ implementation**: Smart contracts are written in a restricted variant of C++ and compiled to native machine code, not bytecode. See [Language Restrictions](/developers/smart-contracts/smart-contract/restrictions) for the full list of enforced rules
- **Direct execution on UEFI ("bare metal")**: Contracts run directly on the Computor hardware through the UEFI layer, without any virtual machine, which is why Qubic achieves such exceptional performance.
- **Deterministic compilation**: The same source code always produces identical executable contracts, ensuring reproducible deployments
- **No runtime interpretation**: Unlike Ethereum's EVM or other VM-based systems, there's no runtime interpretation overhead

## Contract Identification System

Each smart contract is identified by two values:

1. **Contract index** - A numerical identifier assigned to the contract
2. **Contract address** - A 60-character string deterministically derived from the index

Common usage examples:
- The **index** is used in RPC calls like `querySmartContract`
- The **address** is used as the `destination` field when sending transactions to the contract

For example, the **QUTIL** contract has index `4` and address `EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVWRF`, while the **QX** contract has index `1` and address `BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARMID`.

You can find contract indexes and addresses using:

- **Smart contract explorer**: https://explorer.qubic.org/network/assets/smart-contracts
- **Smart contract registry (JSON)**: https://static.qubic.org/v1/general/data/smart_contracts.json (data extracted from the tickchain in JSON format, plus additional metadata useful for app development)

## Functions vs Procedures - Separation of Concerns

### Functions (Read-Only Operations)

- Cannot modify contract state
- Don't require transactions, only RPC queries
- Always return the same result for the same state

Example from QX contract:

```cpp
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

### Procedures (Write Operations)

- Can modify contract state
- Must be invoked through signed transactions
- May require QUs depending on contract logic

Example from QX contract:

```cpp
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

## Registering Functions and Procedures

Each function and procedure must be registered with a unique numeric index to be callable externally.

- **Unique identification**: Each function/procedure has a specific numeric index
- **Public interface**: Defines the contract's available API
- **Validation**: Only registered functions can be invoked externally

Example from QX contract:

```cpp
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

## Development, Review, and Deployment

Every contract developer should be familiar with the full lifecycle of a smart contract, from development to review and deployment on mainnet. See the [Smart Contract Development Guide](https://github.com/qubic/core/blob/main/doc/contracts.md) in the official core repository.
