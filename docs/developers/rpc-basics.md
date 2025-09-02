---
title: RPC Basics
---

# RPC Basics

## Official RPC Documentation

**Complete API reference**: https://qubic.github.io/integration/Partners/qubic-rpc-doc.html?urls.primaryName=Qubic%20RPC%20Live%20Tree

The official RPC documentation provides comprehensive details about all available endpoints, request/response formats, and usage examples. This is your primary reference for implementing Qubic integrations.

## Core RPC Endpoints

### Network Status and Information

**GET /status**

- Returns current network state including tick information, epoch details, and network health metrics
- Essential for determining the current tick before scheduling transactions
- Response includes active tick, current epoch, and network statistics

**`GET /ticks/{tickNumber}`**

- Retrieves detailed information about a specific tick
- Includes all transactions executed in that tick and their results
- Crucial for verifying transaction inclusion and debugging failed executions

### Account and Balance Operations

**`GET /balances/{identityId}`**

- Query QU balance for any identity
- Returns current balance and pending transaction information
- Use the 256-bit public key as the identity identifier

**`GET /assets/{identityId}`**

- Retrieve all assets owned by an identity
- Includes asset names, quantities, and metadata
- Essential for applications dealing with custom tokens

### Smart Contract Interactions

**POST /querySmartContract**

```json
{
  "contractIndex": 1,
  "inputType": 2,
  "inputSize": 40,
  "requestData": "base64EncodedPayload"
}
```

- Execute read-only contract functions
- No transaction required, immediate response
- Response data needs to be decoded based on contract output structure

**POST /broadcastTransaction**

```json
{
  "encodedTransaction": "base64EncodedSignedTransaction"
}
```

- Submit signed transactions to the network
- Transaction must be properly formatted and scheduled for future tick
- Returns transaction ID for tracking

### Transaction Verification

**`GET /transactions/{transactionId}`**

- Check transaction status and inclusion
- Returns execution tick, status, and any error messages
- Essential for confirming transaction success

**`GET /entities/{entityId}`**

- Get detailed entity information including transaction history (where available within current epoch)
- Useful for debugging and account state verification
