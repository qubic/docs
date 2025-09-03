---
sidebar_position: 8
---

# QPI

## What is QPI?

QPI stands for Qubic Programming Interface — a carefully designed and restricted programming interface used to develop smart contracts in the Qubic protocol.

Unlike general-purpose C++ programming, QPI provides a safe, deterministic, and sandboxed environment that ensures all contracts behave consistently across all nodes in the Qubic network. This is essential to maintain consensus and trustless execution.

## Why QPI Exists

In a distributed, consensus-driven system like Qubic, **nondeterminism is dangerous**. If different nodes compute different results from the same contract call, the network breaks down.

QPI solves this by:

- **Restricting unsafe features** of C++ (like pointers, floats, raw memory access).

- **Disallowing standard libraries** to avoid system-dependent behavior.

- **Providing a strict interface** that all contracts must use to interact with the Core and with other contracts.

## What QPI Provides

QPI exposes a minimal but powerful set of features, including:

| Capability                       | Description                                                                                                                                |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Custom Data Types**            | Use safe and deterministic types like `sint64`, `uint32`, `Array`, `BitArray`, `id`, etc.                                                  |
| **Contract Communication**       | Allows sending and receiving messages to/from other contracts.                                                                             |
| **Asset and Share Handling**     | Provides methods to issue, burn, transfer, and manage asset ownership.                                                                     |
| **Tick & Epoch Lifecycle Hooks** | Contracts can react to epoch/tick transitions via `BEGIN_EPOCH()`, `END_TICK()`, etc.                                                      |
| **Contract Metadata Access**     | Access to `qpi.invocator()`, `qpi.originator()`, `qpi.invocationReward()`, and similar context data.                                       |
| **Safe Arithmetic**              | Built-in functions like `div()`, `mod()` to avoid division-by-zero or float precision issues.                                              |
| **Cryptographic Functions**      | Cryptographic functionality through the K12 function, which is based on the KangarooTwelve (K12) hash algorithm.                           |
| **Memory Operations**            | Low-level memory operations for efficiently copying and initializing data structures in smart contracts. eg. `copyMemory()`, `setMemory()` |

## Core QPI Functions

### qpi.invocator()

The `qpi.invocator()` function returns the ID of the entity (user or contract) that directly called the current contract function/procedure.

**Function Signature**

```cpp
id invocator() const
```

**Example usage:**

```cpp
PUBLIC_PROCEDURE(updateBalance)
{
    // Only allow user with public key id(1,2,3,4) to call this
    if (qpi.invocator() != id(1,2,3,4)) {
      return;
    }
    // ... proceed with logic ...
}
```

### qpi.originator()

The `qpi.originator()` function returns the ID of the original transaction sender—the entity (user or contract) that initiated the entire call chain leading to the current contract execution.

**Function Signature**

```cpp
id originator() const
```

**How It Differs from `qpi.invocator()`**

| Function           | Returns                          | Example Call Chain (`Alice → ContractA → ContractB`) |
| ------------------ | -------------------------------- | ---------------------------------------------------- |
| **`originator()`** | Original sender (first in chain) | Inside `ContractB`: `Alice`                          |
| **`invocator()`**  | Immediate caller (last in chain) | Inside `ContractB`: `ContractA`                      |

**Example usage:**

```cpp
PUBLIC_PROCEDURE(updateBalance)
{
    // Only allow direct calls from users (no intermediate contracts)
    // Rejects any calls coming through other contracts in the call chain
    if (qpi.invocator() != qpi.originator()) {
      return;
    }
    // ... proceed with logic ...
}
```

### qpi.invocationReward()

Returns the amount of Qu (Qubic's native token) attached to the current contract call as an invocation reward.

**Function Signature**

```cpp
sint64 invocationReward() const
```

**Paywall Protection Example:**

```cpp
constexpr sint64 FEE = 1000; // 1000 QU required
PUBLIC_PROCEDURE(premiumFeature) {
    if (qpi.invocationReward() < FEE) {
        // user will lost 1000 QUs, because we don't give back
        return;
    }
    // Grant access...
}
```

### qpi.transfer()

Transfers QU (Qubic's native token) from the contract's balance to another address.

**Function Signature**

```cpp
inline sint64 transfer( // Attempts to transfer energy from this qubic
	const id& destination, // Destination to transfer to, use NULL_ID to destroy the transferred energy
	sint64 amount // Energy amount to transfer, must be in [0..1'000'000'000'000'000] range
) const; // Returns remaining energy amount; if the value is less than 0 then the attempt has failed, in this case the absolute value equals to the insufficient amount
```

**1. Basic Transfer**

```cpp
PUBLIC_PROCEDURE_WITH_LOCALS(sendPayment) {
    locals.result = qpi.transfer(input.recipientId, 1000);
    if (locals.result < 0) {
        return;
    }
    // Success: 'result' contains new balance
}
```

**2. Burn QU (Destroy Tokens)**

```cpp
PUBLIC_PROCEDURE_WITH_LOCALS(burnTokens) {
    locals.burned = qpi.transfer(NULL_ID, input.amount);
    // burned = remaining balance
}
```

### qpi.burn()

Permanently removes QU (Qubic's native token) from circulation by burning them from the contract's balance.

**Function Signature**

```cpp
sint64 burn(sint64 amount) const
```

**1. Basic Token Burning**

```cpp
PUBLIC_PROCEDURE_WITH_LOCALS(burnTokens) {
    locals.remaining = qpi.burn(1000); // Burn 1000 QU
    if (locals.remaining < 0) {
       return;
    }
    // Success: 'remaining' shows new balance
}
```

**2. Conditional Burn**

```cpp
PUBLIC_PROCEDURE_WITH_LOCALS(burnExcess) {
    if (state.balance > state.targetBalance) {
        locals.excess = state.balance - state.targetBalance;
        qpi.burn(locals.excess); // Burn surplus QU
    }
}
```

### qpi.K12()

Computes a **KangarooTwelve (K12)** cryptographic hash of input data, returning a 256-bit (32-byte) digest as an `id` type.

**Function Signature**

```cpp
template <typename T>
id K12(const T& data) const
```

**1. Hashing Raw Data**

```cpp
struct HashExample_input {
  Array<uint8, 2> rawData;
};

struct HashExample_output {
  id hashResult;
};

PUBLIC_FUNCTION(HashExample) {
  // Compute K12 hash
  output.hashResult = qpi.K12(input.rawData);
}
```

**2. Creating Unique IDs**

```cpp
struct User {
  id publicKey;
  uint32 registrationDate;
};

struct createUserId_input {
  id pub;
};

struct createUserId_output {
  id hash;
};

struct createUserId_locals {
  User user;
};

PUBLIC_FUNCTION_WITH_LOCALS(createUserId) {
  locals.user = { input.pub, qpi.tick() };
  output.hash = qpi.K12(locals.user); // Deterministic ID
}
```

### qpi.issueAsset()

The `issueAsset()` function allows smart contracts to create `new digital assets` on the Qubic network. These assets can represent anything from currencies to physical commodities.

**Function Signature**

```cpp
sint64 issueAsset(
  uint64 assetName,
  id issuer,
  sint8 decimalPlaces,
  sint64 numberOfShares,
  uint64 unitOfMeasurement
)
```

**Parameters**

| Parameter             | Type     | Range                 | Description                                   | Example Value         |
| --------------------- | -------- | --------------------- | --------------------------------------------- | --------------------- |
| **assetName**         | `uint64` | 0 to 2<sup>64</sup>-1 | 8-byte asset identifier (ASCII or hex)        | `0x444C4F47` ("GOLD") |
| **issuer**            | `id`     | 256-bit               | Owner's public key (must match caller)        | `id(_A,_B,...,_Z)`    |
| **decimalPlaces**     | `sint8`  | -128 to 127           | Number of decimal digits for fractional units | `3` (milli-units)     |
| **numberOfShares**    | `sint64` | 1 to 2<sup>63</sup>-1 | Total supply to mint (must be positive)       | `1_000_000`           |
| **unitOfMeasurement** | `uint64` | 0 to 2<sup>64</sup>-1 | Physical unit code (ASCII or hex)             | `0x6B67` ("kg")       |

**Key Notes:**

1. **Uniqueness**: `assetName` must be unique per issuer
2. **Authorization**: Caller must be the `issuer`
3. **Precision**: Negative `decimalPlaces` are allowed but uncommon
4. **Unit Codes**: Use SI unit abbreviations in hex

**Example Use Case**

```cpp
// Issue 1M "SILVER" tokens with gram precision
output.issuedShares = qpi.issueAsset(
  0x5245564c4953,  // "SILVER"
  issuerId,
  3,               // 3 decimal places (grams)
  1'000'000,       // 1M units
  0x6772616D       // "gram" in hex
);
```

:::info
The functions `assetNameFromString` and `assetNameFromInt64` are useful in tests for converting asset names between string and `int64` formats.
:::

### qpi.transferShareOwnershipAndPossession()

Transfers both **legal ownership** and **physical possession** of asset shares in a single atomic operation. This is the most comprehensive asset transfer function in Qubic, combining two critical rights transfers into one call.

**Function Signature**

```cpp
sint64 transferShareOwnershipAndPossession(
  uint64 assetName,
  id issuer,
  id owner,
  id possessor,
  sint64 numberOfShares,
  id newOwnerAndPossessor
)
```

| Parameter                  | Type     | Description                                                                | Required | Example Values        |
| -------------------------- | -------- | -------------------------------------------------------------------------- | -------- | --------------------- |
| **`assetName`**            | `uint64` | Unique 8-byte asset identifier (ASCII or hex encoded)                      | Yes      | `0x474F4C44` ("GOLD") |
| **`issuer`**               | `id`     | 256-bit address of the original asset creator                              | Yes      | `ID(_A, _B,...,_Z)`   |
| **`owner`**                | `id`     | Current legal owner's address                                              | Yes      | `ID(_C, _B,...,_Y)`   |
| **`possessor`**            | `id`     | Current holder's address (may differ from owner in custodial arrangements) | Yes      | `ID(_E, _B,...,_Z)`   |
| **`numberOfShares`**       | `sint64` | Positive quantity of shares to transfer (1 to 2<sup>63</sup>-1)            | Yes      | `500`                 |
| **`newOwnerAndPossessor`** | `id`     | Recipient address or (`NULL_ID` burns shares)                              | Yes      | `ID(_B, _B,...,_D)`   |

**Special Values**

- `NULL_ID` for `newOwnerAndPossessor`: Permanently burns the specified shares
- Zero `numberOfShares`: Transaction will fail with `INVALID_AMOUNT` error

**Authorization Rules**

The caller must be:

1. The current **owner** (for ownership transfer)  
   **OR**
2. The current **possessor** (for possession transfer)  
   **OR**
3. An authorized **managing contract**

**Example Usage:**

```cpp
// Transfer 100 "SILVER" shares from Alice to Bob
qpi.transferShareOwnershipAndPossession(
  0x53494C564552,  // "SILVER"
  issuerId,        // Original creator
  aliceId,         // Current owner
  aliceId,         // Current possessor (self-custody)
  100,             // Shares to transfer
  bobId            // New owner/possessor
);

// Burn 50 shares
qpi.transferShareOwnershipAndPossession(
  0x474F4C44,
  issuerId,
  ownerId,
  ownerId,
  50,
  NULL_ID          // Burn target
);
```

### qpi.numberOfShares()

Gets the total supply or user-specific balances of asset shares.

**Function Signature**

```cpp
sint64 numberOfShares(
  const Asset& asset,
  const AssetOwnershipSelect& ownership = AssetOwnershipSelect::any(),
  const AssetPossessionSelect& possession = AssetPossessionSelect::any()
) const
```

**Common Use Cases**

**1. Get Total Asset Supply**

```cpp
Asset gold = {issuerId, 0x474F4C44}; // "GOLD"
sint64 totalSupply = qpi.numberOfShares(gold);
```

**2. Check User Balance**

```cpp
sint64 userBalance = qpi.numberOfShares(
  gold,
  AssetOwnershipSelect::byOwner(userId), // Filter by owner
  AssetPossessionSelect::byPossessor(userId) // Filter by holder
);
```

**3. Check Managed Assets**

```cpp
// Get shares managed by specific contract
sint64 managedShares = qpi.numberOfShares(
  gold,
  AssetOwnershipSelect::byManagingContract(contractIndex),
  AssetPossessionSelect::any()
);
```

**Filter Options**

For ownership/possession filters:

```cpp
// Ownership filters
AssetOwnershipSelect::any() // All owners
AssetOwnershipSelect::byOwner(specificId) // Specific owner
AssetOwnershipSelect::byManagingContract(index) // Managed by contract

// Possession filters
AssetPossessionSelect::any() // All possessors
AssetPossessionSelect::byPossessor(specificId) // Specific holder
AssetPossessionSelect::byManagingContract(index) // Managed by contract
```

### qpi.releaseShares()

Mention in [Assets And Shares](/smart-contract/assets-and-shares)

### qpi.acquireShares()

Mention in [Assets And Shares](/smart-contract/assets-and-shares)

### qpi.getEntity()

Retrieves entity information (balance, transaction stats) from the Qubic ledger.

**Function Signature**

```cpp
bool getEntity(
  const id& entityId,
  Entity& outputEntity
) const
```

**Usage Examples**

**_1. Basic Entity Lookup_**

```cpp
struct getUserEntity_input {
  id userId;
};

struct getUserEntity_output {
  QPI::Entity userEntity;
  sint64 netFlow;
};

PUBLIC_FUNCTION(getUserEntity) {
  if (qpi.getEntity(input.userId, output.userEntity)) {
    // Use entity data
    output.netFlow = output.userEntity.incomingAmount - output.userEntity.outgoingAmount;
  } else {
    // Entity not found
  }
}
```

### qpi.year|month|day|hour|minute|second|millisecond|tick|epoch|dayOfWeek()

These functions provide access to the current date, time, and blockchain-specific timestamps

:::note
All time/date functions return **UTC** values
:::

:::warning
In the test environment, these functions will not work correctly—they will always return `0` unless an extra step is performed. This will be explained later.
:::

```cpp
struct GetDateTime_input {
  // Can be empty or contain parameters
};

struct GetDateTime_output {
  uint8  year;
  uint8  month;
  uint8  day;
  uint8  hour;
  uint8  minute;
  uint8  second;
  uint16 millisecond;
  uint32 tick;
  uint16 epoch;
};

PUBLIC_FUNCTION(GetDateTime) {
  // Get current date/time
  output.year = qpi.year();         // 0-99 (2000-2099)
  output.month = qpi.month();       // 1-12
  output.day = qpi.day();           // 1-31

  // Get current time
  output.hour = qpi.hour();         // 0-23
  output.minute = qpi.minute();     // 0-59
  output.second = qpi.second();     // 0-59
  output.millisecond = qpi.millisecond(); // 0-999

  // Get Qubic-specific timings
  output.tick = qpi.tick();         // Current tick
  output.epoch = qpi.epoch();       // Current epoch
}

struct DayOfWeek_input {
  uint8 year;
  uint8 month;
  uint8 day;
};

struct DayOfWeek_output {
  uint8 dayOfWeek; // 0=Wednesday, 1=Thursday,...6=Tuesday
};

PUBLIC_FUNCTION(DayOfWeek) {
  output.dayOfWeek = qpi.dayOfWeek(
    input.year,
    input.month,
    input.day
  );
}
```
