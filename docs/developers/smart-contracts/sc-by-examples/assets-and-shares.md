# Assets And Shares

[**Source Code**](https://github.com/hackerby888/qubic-sc-examples/tree/assets-and-shares)

## MYTEST Contract

### Overview

A contract for issuing and managing asset shares with fixed transfer fees.

### Key Features:

1. **Asset Issuance**

   - Creates new assets with customizable parameters
   - Sets initial share distribution

2. **Share Release**
   - Transfers shares to other contracts
   - Implements fixed fee structure

### Core Functions

#### `issueAsset`

```cpp
struct issueAsset_input {
    uint64 name;                      // Asset identifier
    id issuer;                       // Creator's Qubic ID
    sint8 decimalPlaces;             // Precision (e.g., 8 for BTC-like)
    sint64 numberOfShares;          // Initial supply
    uint64 unitOfMeasurement;      // Measurement standard
};

struct issueAsset_output {
    bit success;
};
```

- Wraps QPI's native asset creation

- Returns success/failure status

#### `releaseShares`

```cpp
struct releaseShares_input {
    Asset asset;                    // Asset to transfer
    id owner;                      // Current owner
    id possessor;                 // Current holder
    sint64 numberOfShares;       // Amount to release
    uint16 destOwnershipContract; // Receiving contract
    uint16 destPossessionContract;
    sint64 offeredFee;          // Must match fixed fee
};

struct releaseShares_output {
    bit success;
};
```

- Transfers shares between contracts

- Enforces 100 QU fixed fee via `PRE_RELEASE_SHARES`

- Atomic transfer - either fully completes or fails

## CROSS Contract

### Overview

A counterpart contract designed to receive asset shares from MYTEST.

### Key Features:

#### 1. Share Acquisition

- Accepts incoming share transfers

- Implements matching fee structure

#### 2. Inter-contract Compatibility

- Designed to work with MYTEST's release mechanism

- Mirror image fee validation

### Core Function

#### acquireShares

```cpp
struct acquireShares_input {
    Asset asset;                   // Asset being received
    id owner;                     // Original owner
    id possessor;                // Sender
    sint64 numberOfShares;      // Amount
    uint16 srcOwnershipContract; // Sending contract
    uint16 srcPossessionContract;
    sint64 offeredFee;         // Must > requestedFee
};

struct acquireShares_output {
  bit success;
};
```

- Receives shares released from `srcOwnershipContract`/`srcPossessionContract`

- Validates 100 QU fee in pre-transfer hook

- Returns success/failure status

## Interaction Flow

### releaseShares

- MYTEST calls `releaseShares`

- CROSS's `PRE_ACQUIRE_SHARES` validates fee

- Qubic SC executes atomic transfer

- Both contracts update their states

- CROSS's `POST_ACQUIRE_SHARES` validates fee

### acquireShares

- CROSS calls `acquireShares`

- MYTEST's `PRE_RELEASE_SHARES` validates fee

- Qubic SC executes atomic transfers

- Both contracts update their states

- MYTEST's `PRE_RELEASE_SHARES` is invoked
