---
title: Complete Transaction Example
---

# Complete Transaction Example

## Introduction

This section demonstrates how to construct payloads for QX smart contract interactions. QX is Qubic's decentralized exchange (contract index 1), and these examples show the most common operations developers need to implement.

## Understanding QX Operations

### QX Contract Identification

Before constructing any QX transaction, you need to understand the dual identification system. The contract address is what you use as the destination in transactions, while the index is used for querySmartContract calls.

```javascript
const QX_CONTRACT = {
  index: 1, // Used for RPC queries
  address: "BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARMID", // Used for transactions
};
```

### Procedure Numbers

QX procedures have specific numeric identifiers that you must use as inputType. These numbers correspond to the registration order in the QX contract's REGISTER_USER_FUNCTIONS_AND_PROCEDURES() section.

```javascript
const QX_PROCEDURES = {
  ISSUE_ASSET: 1,
  TRANSFER_SHARES: 2,
  ADD_TO_ASK_ORDER: 5, // Sell order
  ADD_TO_BID_ORDER: 6, // Buy order
  REMOVE_FROM_ASK_ORDER: 7,
  REMOVE_FROM_BID_ORDER: 8,
};
```

## Example: QX Bid Order

### Conceptual Understanding

A bid order is how you buy assets on QX. When you place a bid order, you're saying "I want to buy X amount of asset Y at price Z". The QX contract will:

1. Lock your QU in escrow (price × numberOfShares)
2. Try to match your bid with existing ask orders
3. If no match, keep your order in the order book until someone sells at your price

### C++ Structure Analysis

Before constructing the payload, examine the C++ struct from the QX contract. This defines exactly what data the contract expects and in what order:

```cpp
struct AddToBidOrder_input {
    id issuer;              // 32 bytes (PublicKey of asset creator)
    uint64 assetName;       // 8 bytes (asset name as number)
    sint64 price;           // 8 bytes (price per share in QU)
    sint64 numberOfShares;  // 8 bytes (how many shares to buy)
};
// Total size: 32 + 8 + 8 + 8 = 56 bytes
```

### Step-by-Step Implementation

#### Step 1: Import Required Libraries

First, we need to import all the required types from the Qubic TypeScript library. These provide the essential building blocks for constructing transactions:

```javascript
import { QubicTransaction } from "@qubic-lib/qubic-ts-library/dist/qubic-types/QubicTransaction";
import { PublicKey } from "@qubic-lib/qubic-ts-library/dist/qubic-types/PublicKey";
import { Long } from "@qubic-lib/qubic-ts-library/dist/qubic-types/Long";
import { DynamicPayload } from "@qubic-lib/qubic-ts-library/dist/qubic-types/DynamicPayload";
import { QubicPackageBuilder } from "@qubic-lib/qubic-ts-library/dist/QubicPackageBuilder";
```

#### Step 2: Payload Construction Function

Now we'll build the payload construction function piece by piece.

**Function signature and size calculation:**
We start by defining the function and calculating the exact payload size that matches the C++ struct:

```javascript
function createQXBidOrderPayload({ issuer, assetName, price, numberOfShares }) {
  // Total payload size:
  // id issuer = 32 bytes
  // uint64 assetName = 8 bytes
  // sint64 price = 8 bytes
  // sint64 numberOfShares = 8 bytes
  // Total = 56 bytes
  const packageSize = 56;

  const builder = new QubicPackageBuilder(packageSize);
```

**Adding the issuer field:**
The first field is the issuer ID, which is a 32-byte PublicKey representing who created the asset:

```javascript
// 1. issuer (id = PublicKey, 32 bytes)
builder.add(new PublicKey(issuer));
```

**Asset name conversion and addition:**
The asset name needs to be converted from a string to a uint64 number. We handle both string and numeric inputs:

```javascript
// 2. assetName (uint64, 8 bytes)
// Convert string to number if necessary
let assetNameValue;
if (typeof assetName === "string") {
  // Convert string to uint64 (example: "CFB" -> number)
  const encoder = new TextEncoder();
  const bytes = encoder.encode(assetName.padEnd(8, "\0"));
  const view = new DataView(bytes.buffer);
  assetNameValue = view.getBigUint64(0, true); // little endian
} else {
  assetNameValue = BigInt(assetName);
}
builder.add(new Long(assetNameValue));
```

**Adding price and share count:**
The final two fields are straightforward numeric values, both converted to BigInt to handle large numbers safely:

```javascript
// 3. price (sint64, 8 bytes)
builder.add(new Long(BigInt(price)));

// 4. numberOfShares (sint64, 8 bytes)
builder.add(new Long(BigInt(numberOfShares)));
```

**Creating the final payload:**
Finally, we package all the data into a DynamicPayload object that can be used in the transaction:

```javascript
  const payload = new DynamicPayload(packageSize);
  payload.setPayload(builder.getData());

  return payload;
}
```

#### Step 3: Complete Transaction Function

Now we'll build the main transaction function that puts everything together.

**Function signature and payload creation:**
We start by accepting all the necessary parameters and creating the payload using our helper function:

```javascript
export async function runQXBidOrder({
  rpc,
  seed,
  sourcePublicKey,
  contractAddress,
  issuer,
  assetName,
  price,
  numberOfShares,
  targetTick,
}) {
  // Create payload for AddToBidOrder (inputType 6)
  const payload = createQXBidOrderPayload({
    issuer,
    assetName,
    price,
    numberOfShares,
  });

  // Calculate total amount (price * numberOfShares)
  const totalAmount = price * numberOfShares;
```

**Building the transaction:**
Next, we construct the QubicTransaction object with all the required fields. The amount represents QU that will be locked in escrow:

```javascript
// Create transaction
const transaction = new QubicTransaction()
  .setSourcePublicKey(new PublicKey(sourcePublicKey))
  .setDestinationPublicKey(new PublicKey(contractAddress))
  .setTick(targetTick)
  .setInputType(6) // AddToBidOrder
  .setInputSize(payload.getPackageSize())
  .setAmount(new Long(BigInt(totalAmount)))
  .setPayload(payload);
```

**Signing and broadcasting:**
Finally, we sign the transaction with the private key (derived from seed) and broadcast it to the network:

```javascript
// Sign transaction
await transaction.build(seed);

// Send transaction
const result = await broadcastTransaction(transaction, rpc);
```

**Return structured response:**
The function returns detailed information about both the transaction and the broadcast result:

```javascript
  return {
    transaction: {
      sourcePublicKey,
      destinationPublicKey: contractAddress,
      tick: targetTick,
      inputType: 6,
      amount: totalAmount,
      inputSize: payload.getPackageSize(),
    },
    payload: {
      issuer,
      assetName,
      price,
      numberOfShares,
    },
    broadcast: result,
  };
}
```

#### Step 4: Broadcast Helper Function

The broadcast function handles the actual network communication.

**Transaction encoding:**
First, we encode the signed transaction to base64 format for HTTP transmission:

```javascript
async function broadcastTransaction(transaction, rpcUrl) {
  const encodedTransaction = transaction.encodeTransactionToBase64(
    transaction.getPackageData()
  );

  const request = {
    encodedTransaction: encodedTransaction,
  };
```

**Network request:**
Then we send the encoded transaction to the Qubic RPC endpoint:

```javascript
const response = await fetch(`${rpcUrl}v1/broadcast-transaction`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(request),
});
```

**Error handling and response:**
Finally, we check for HTTP errors and return the JSON response:

```javascript
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}
```

### Usage Example

Here's how to use the complete implementation with real working values:

```javascript
// Buy 100 CFB tokens at 4 QU each - using real working configuration
const result = await runQXBidOrder({
  rpc: "https://testnet-rpc.qubicdev.com/",
  seed: "fwqatwliqyszxivzgtyyfllymopjimkyoreolgyflsnfpcytkhagqii",
  sourcePublicKey: "YOUR_PUBLIC_KEY_HERE",
  contractAddress:
    "BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARMID",
  issuer: "GARTHFANXMPXMDPEZFQPWFPYMHOAWTKILINCTRMVLFFVATKVJRKEDYXGHJBF",
  assetName: "CFB",
  price: 4,
  numberOfShares: 100,
  targetTick: currentTick + 30,
});
```

This will lock 400 QU in escrow and create a buy order for CFB tokens.

## Complete Functions Reference

Here are the complete functions assembled from all the explained fragments:

### createQXBidOrderPayload (Complete)

```javascript
function createQXBidOrderPayload({ issuer, assetName, price, numberOfShares }) {
  // Total payload size:
  // id issuer = 32 bytes
  // uint64 assetName = 8 bytes
  // sint64 price = 8 bytes
  // sint64 numberOfShares = 8 bytes
  // Total = 56 bytes
  const packageSize = 56;

  const builder = new QubicPackageBuilder(packageSize);

  // 1. issuer (id = PublicKey, 32 bytes)
  builder.add(new PublicKey(issuer));

  // 2. assetName (uint64, 8 bytes)
  // Convert string to number if necessary
  let assetNameValue;
  if (typeof assetName === "string") {
    // Convert string to uint64 (example: "CFB" -> number)
    const encoder = new TextEncoder();
    const bytes = encoder.encode(assetName.padEnd(8, "\0"));
    const view = new DataView(bytes.buffer);
    assetNameValue = view.getBigUint64(0, true); // little endian
  } else {
    assetNameValue = BigInt(assetName);
  }
  builder.add(new Long(assetNameValue));

  // 3. price (sint64, 8 bytes)
  builder.add(new Long(BigInt(price)));

  // 4. numberOfShares (sint64, 8 bytes)
  builder.add(new Long(BigInt(numberOfShares)));

  const payload = new DynamicPayload(packageSize);
  payload.setPayload(builder.getData());

  return payload;
}
```

### runQXBidOrder (Complete)

```javascript
export async function runQXBidOrder({
  rpc,
  seed,
  sourcePublicKey,
  contractAddress,
  issuer,
  assetName,
  price,
  numberOfShares,
  targetTick,
}) {
  // Create payload for AddToBidOrder (inputType 6)
  const payload = createQXBidOrderPayload({
    issuer,
    assetName,
    price,
    numberOfShares,
  });

  // Calculate total amount (price * numberOfShares)
  const totalAmount = price * numberOfShares;

  // Create transaction
  const transaction = new QubicTransaction()
    .setSourcePublicKey(new PublicKey(sourcePublicKey))
    .setDestinationPublicKey(new PublicKey(contractAddress))
    .setTick(targetTick)
    .setInputType(6) // AddToBidOrder
    .setInputSize(payload.getPackageSize())
    .setAmount(new Long(BigInt(totalAmount)))
    .setPayload(payload);

  // Sign transaction
  await transaction.build(seed);

  // Send transaction
  const result = await broadcastTransaction(transaction, rpc);

  return {
    transaction: {
      sourcePublicKey,
      destinationPublicKey: contractAddress,
      tick: targetTick,
      inputType: 6,
      amount: totalAmount,
      inputSize: payload.getPackageSize(),
    },
    payload: {
      issuer,
      assetName,
      price,
      numberOfShares,
    },
    broadcast: result,
  };
}
```

### broadcastTransaction (Complete)

```javascript
async function broadcastTransaction(transaction, rpcUrl) {
  const encodedTransaction = transaction.encodeTransactionToBase64(
    transaction.getPackageData()
  );

  const request = {
    encodedTransaction: encodedTransaction,
  };

  const response = await fetch(`${rpcUrl}v1/broadcast-transaction`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}
```

## Common Pitfalls and Debugging

### Payload Size Errors

**Problem**: Transaction rejected with "invalid input size"

**Solution**: Double-check your C++ struct size calculation:

- `AddToBidOrder`: exactly 56 bytes
- Use `payload.getPackageSize()` to verify

### Insufficient QU Balance

**Problem**: Transaction fails with insufficient balance

**Solution**: For bid orders, you need `price × numberOfShares` QU available plus any transaction fees.

### Wrong Tick Timing

**Problem**: Transaction never executes

**Solution**: Use adequate tick offset (30+ for smart contracts) and verify current tick before sending.
