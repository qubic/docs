---
title: Qubic Programming Interface (QPI)
---

# Qubic Programming Interface (QPI)

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
| **Contract Communication**       | Allows running procedures and functions of other contracts.                                                                                |
| **Asset and Share Handling**     | Provides methods to issue, burn, transfer, and manage asset ownership.                                                                     |
| **Tick & Epoch Lifecycle Hooks** | Contracts can react to epoch/tick transitions via `BEGIN_EPOCH()`, `END_TICK()`, etc.                                                      |
| **Contract Metadata Access**     | Access to `qpi.invocator()`, `qpi.originator()`, `qpi.invocationReward()`, and similar context data.                                       |
| **Safe Arithmetic**              | Built-in functions like `div()`, `mod()` to avoid division-by-zero or float precision issues.                                              |
| **Cryptographic Functions**      | Cryptographic functionality through the K12 function, which is based on the KangarooTwelve (K12) hash algorithm.                           |
| **Memory Operations**            | Low-level memory operations for efficiently copying and initializing data structures in smart contracts. eg. `copyMemory()`, `setMemory()` |

`qpi.h` is the Qubic Programming Interface for implementing the smart contracts. It is available automatically in the smart contract implementation header files. This page outlines the guidelines for developing secure and efficient Qubic contracts.
Adherence to these guidelines is crucial for ensuring the proper functionality and security of your contracts within the Qubic environment.

## Concepts

The state is the persistent memory of the contract that is kept aligned in all nodes. A contract can have member functions and procedures.

Functions cannot change the state of the contract. They can be called via a `RequestContractFunction` network message.

Procedures can change the state of the contract. They are invoked by a transaction and run when the tick containing the transaction is processed.

There are some special procedures that are called by the system at the beginning of the tick etc.

A call of a user procedure usually goes along with a transfer of an invocation reward from the invoking user to the contract.

Procedures can call procedures and functions of the same contract and of contracts with lower contract index.

Functions can call functions of the same contract and of contracts with lower contract ID.

Private functions and procedures cannot be called from other contracts.

In order to be available for invocation by transaction and network message, procedures and functions need to be registered in the special member function `REGISTER_USER_FUNCTIONS_AND_PROCEDURES`.

## Syntax and Formatting

Due to security reasons, certain things are prohibited:

- Declaring and accessing arrays using the C/C++ notation (`[` `]`). Utilize pre-defined array structures within qpi.h such as `collection`, `uint32_64`, `uint32_128`, ...
- Any pointer-related techniques such as casting, accessing, ...
- Native data types like `bool`, `int`, `long`, `char`, ... Use their corresponding predefined data types in `qpi.h` (`bit`, `uint8`, `sint8`, `uint16`, `sint32`, `uint64`, ...)
- Inclusion of other files via `#include`. All functions must reside within a single file.
- Math operators `%` and `/`. Use `mod` and `div` from `qpi.h` instead. `+`, `-`, `*`(multiplication), and bit-wise operators are accepted.
- Local variable declaration, even for for-loop. You need to define all necessary variables in either in the contract state or in a "locals" struct similar to the input and output struct of a function or procedure.
- The `typedef`, `union` keyword.
- Floating point data types (half, float, double)

Currently, the maximum contract state size is capped at 1 GiB (03/02/2024). This value is subject to change based on hardware upgrades of computors.

## Member Variables and Functions:

- struct `bit_x` (x = 2 ^ n, n = 1 ~ 24)
  - Member Variable
    - uint64 \_values : `x-bit` integer
  - Member function
    - bit get(uint64 index) : Retrieves the `index`-th bit of `_values`
    - void set(uint64 index, bit value) : Sets at the specified `index`-th bit to the provided bit `value`
- struct `sint8_x` (x = 2 ^ n, n = 1 ~ 24)
  - Member Variable
    - sint8 \_values[x]; : An array of x `signed char` elements
  - Member function
    - sint8 get(uint64 index) : Retrieves the element at the specified `index`
    - void set(uint64 index, sint8 value) : Sets the element at the specified `index` to the provided `value`
- The same goes for `uint8_x`, `sint16_x`, `uint16_x`, `sint32_x`, `uint32_x`, `sint64_x`, `uint64_x`, `id_x`.
- struct `collection`

This shows collection of priority queue of elements with type T and total element capacity L.

Each ID pov (point of view) has an own queue.

Array of elements (filled sequentially), each belongs to one PoV / priority queue (or is empty).

Elements of a POV entry will be stored as a binary search tree (BST): so this structure has some properties related to BST(bstParentIndex, bstLeftIndex, bstRightIndex).

Look at the [Binary Search Tree](https://www.geeksforgeeks.org/binary-search-tree-data-structure) to learn more.

- Difference between standard BST and POV BST

Each node in a standard BST has left child containing values less than the parent node and the right child containing values greater than the parent node.

But each element in a POV BST has left child containing `priority` greater than the parent element and the right child containing `priority` less than the parent node.

```cpp
sint64 add(const id& pov, T element, sint64 priority)
```

Add element to priority queue of ID pov, return elementIndex of new element

```cpp
uint64 capacity()
```

Return maximum number of elements that may be stored

```cpp
T element(sint64 elementIndex)
```

Return element value at elementIndex

```cpp
sint64 headIndex(const id& pov)
```

Return elementIndex of first element in priority queue of pov (or NULL_INDEX if pov is unknown)

```cpp
headIndex(const id& pov, sint64 maxPriority)
```

Return elementIndex of first element with priority `<=` maxPriority in priority queue of pov (or NULL_INDEX if pov is unknown)

```cpp
sint64 nextElementIndex(sint64 elementIndex)
```

Return elementIndex of next element in priority queue (or NULL_INDEX if this is the last element)

```cpp
uint64 population() const
```

Return overall number of elements

```cpp
id pov(sint64 elementIndex) const
```

Return point of view elementIndex belongs to (or 0 id if unused)

```cpp
sint64 prevElementIndex(sint64 elementIndex) const
```

Return elementIndex of previous element in priority queue (or NULL_INDEX if this is the last element)

```cpp
sint64 priority(sint64 elementIndex) const
```

Return priority of elementIndex (or 0 id if unused)

```cpp
sint64 remove(sint64 elementIdx)
```

Remove element and mark its pov for removal, if the last element.

Returns element index of next element in priority queue (the one following elementIdx).

Element indices obtained before this call are invalidated, because at least one element is moved.

```cpp
void replace(sint64 oldElementIndex, const T& newElement)
```

Replace _existing_ element, do nothing otherwise.

The element exists: replace its value.

The index is out of bounds: no action is taken.

```cpp
void reset()
```

Reinitialize as empty collection

```cpp
sint64 tailIndex(const id& pov) const
```

Return elementIndex of last element in priority queue of pov (or NULL_INDEX if pov is unknown)

```cpp
sint64 tailIndex(const id& pov, sint64 minPriority) const
```

Return elementIndex of last element with priority >= minPriority in priority queue of pov (or NULL_INDEX if pov is unknown).

## Core QPI Functions

### qpi.invocator()

The `qpi.invocator()` function returns the ID of the entity (user or contract) that directly called the current **contract procedure**.

:::info
`qpi.invocator()` returns a zero public key when called inside a function, because it is triggered by a network message and therefore has no associated entity.

**Exception:** If a function is called inside a procedure, `qpi.invocator()` will return the invocator of the procedure.
:::

**Function Signature**

```cpp
id invocator() const
```

**Example usage:**

```cpp
PUBLIC_PROCEDURE(updateBalance)
{
    // Only allow user with public key id(1,2,3,4) to call this
    if (qpi.invocator() != id(1,2,3,4))
    {
      return;
    }
    // ... proceed with logic ...
}
```

### qpi.originator()

The `qpi.originator()` function returns the ID of the original transaction sender—the entity (user or contract) that initiated the entire call chain leading to the current contract execution.

:::info
`qpi.originator()` returns a zero public key when called inside a function, because it is triggered by a network message and therefore has no associated entity.

**Exception:** If a function is called inside a procedure, `qpi.originator()` will return the originator of the procedure.
:::

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
    if (qpi.invocator() != qpi.originator())
    {
      return;
    }
    // ... proceed with logic ...
}
```

### qpi.invocationReward()

Returns the amount of Qu (Qubic's native token) attached to the current contract call as an invocation reward.

:::info
`qpi.invocationReward()` returns zero when called inside a function, since it is triggered by a network message rather than a transaction, and therefore no reward amount is specified.

**Exception:** If a function is called inside a procedure, `qpi.invocationReward()` will return the reward amount of the procedure.
:::

**Function Signature**

```cpp
sint64 invocationReward() const
```

**Paywall Protection Example:**

```cpp
constexpr sint64 FEE = 1000; // 1000 QU required
PUBLIC_PROCEDURE(premiumFeature)
{
    if (qpi.invocationReward() < FEE)
    {
        // user will lose 1000 QUs, because we don't give back
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
PUBLIC_PROCEDURE_WITH_LOCALS(sendPayment)
{
    locals.result = qpi.transfer(input.recipientId, 1000);
    if (locals.result < 0)
    {
        return;
    }
    // Success: 'result' contains new balance
}
```

**2. Burn QU (Destroy Tokens)**

```cpp
PUBLIC_PROCEDURE_WITH_LOCALS(burnTokens)
{
    locals.burned = qpi.transfer(NULL_ID, input.amount);
    // burned = remaining balance
}
```

### qpi.burn()

Permanently removes QU (Qubic's native token) from circulation by burning them from the contract's balance.

:::info
In the future, contracts will be required to burn QU in order to remain active.
:::

**Function Signature**

```cpp
sint64 burn(sint64 amount) const
```

**1. Basic Token Burning**

```cpp
PUBLIC_PROCEDURE_WITH_LOCALS(burnTokens)
{
    locals.remaining = qpi.burn(1000); // Burn 1000 QU
    if (locals.remaining < 0)
    {
       return;
    }
    // Success: 'remaining' shows new balance
}
```

**2. Conditional Burn**

```cpp
PUBLIC_PROCEDURE_WITH_LOCALS(burnExcess)
{
    if (state.balance > state.targetBalance)
    {
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
struct HashExample_input
{
  Array<uint8, 2> rawData;
};

struct HashExample_output
{
  id hashResult;
};

PUBLIC_FUNCTION(HashExample)
{
  // Compute K12 hash
  output.hashResult = qpi.K12(input.rawData);
}
```

**2. Creating Unique IDs**

```cpp
struct User
{
  id publicKey;
  uint32 registrationDate;
};

struct createUserId_input
{
  id pub;
};

struct createUserId_output
{
  id hash;
};

struct createUserId_locals
{
  User user;
};

PUBLIC_FUNCTION_WITH_LOCALS(createUserId)
{
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

| Parameter             | Type     | Range                                                        | Description                                    | Example Value         |
| --------------------- | -------- | ------------------------------------------------------------ | ---------------------------------------------- | --------------------- |
| **assetName**         | `uint64` | Up to 7 upper case from A-Z characters (encoded to `uint64`) | 8-byte asset identifier (ASCII or hex)         | `0x444C4F47` ("GOLD") |
| **issuer**            | `id`     | 256-bit                                                      | Initial owner's public key (must match caller) | `id(_A,_B,...,_Z)`    |
| **decimalPlaces**     | `sint8`  | -128 to 127                                                  | Number of decimal digits for fractional units  | `3` (milli-units)     |
| **numberOfShares**    | `sint64` | `1` to `1000000000000000`                                    | Total supply to mint (must be positive)        | `1_000_000`           |
| **unitOfMeasurement** | `uint64` | 0 to 2<sup>64</sup>-1                                        | Physical unit code (ASCII or hex)              | `0x6B67` ("kg")       |

**Key Notes:**

1. **Uniqueness**: `assetName` must be unique per issuer
2. **Authorization**: Caller must be the `issuer` (caller can be `qpi.invocator()` or current contract `SELF`)
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
| **`numberOfShares`**       | `sint64` | Positive quantity of shares to transfer (`1` to `1000000000000000`)        | Yes      | `500`                 |
| **`newOwnerAndPossessor`** | `id`     | Recipient address or (`NULL_ID` burns shares)                              | Yes      | `ID(_B, _B,...,_D)`   |

**Special Values**

- `NULL_ID` for `newOwnerAndPossessor`: Permanently burns the specified shares
- Zero `numberOfShares`: Transaction will fail with `INVALID_AMOUNT` error

**Authorization Rules**

The caller must be:

The **managing contract**

:::info
It’s up to the **managing contract** to define the rules (e.g., whether a possessor can reassign possession).
:::

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
AssetOwnershipSelect{specificId, index} // Specific owner and contract

// Possession filters
AssetPossessionSelect::any() // All possessors
AssetPossessionSelect::byPossessor(specificId) // Specific holder
AssetPossessionSelect::byManagingContract(index) // Managed by contract
AssetPossessionSelect{specificId, index} // Specific holder and contract
```

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
struct getUserEntity_input
{
  id userId;
};

struct getUserEntity_output
{
  QPI::Entity userEntity;
  sint64 balance;
};

PUBLIC_FUNCTION(getUserEntity)
{
  if (qpi.getEntity(input.userId, output.userEntity))
  {
    // Use entity data
    output.balance = output.userEntity.incomingAmount - output.userEntity.outgoingAmount;
  }
  else
  {
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
struct getDateTime_input
{
  // Can be empty or contain parameters
};

struct getDateTime_output
{
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

PUBLIC_FUNCTION(getDateTime)
{
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

struct dayOfWeek_input
{
  uint8 year;
  uint8 month;
  uint8 day;
};

struct dayOfWeek_output
{
  uint8 dayOfWeek; // 0=Wednesday, 1=Thursday,...6=Tuesday
};

PUBLIC_FUNCTION(dayOfWeek)
{
  output.dayOfWeek = qpi.dayOfWeek(
    input.year,
    input.month,
    input.day
  );
}
```

For more detailed examples and advanced usage, see our [Smart Contract Examples](smart-contracts/sc-by-examples/assets-and-shares.md) and [Contract Structure Guide](smart-contracts/smart-contract/contract-structure.md).
