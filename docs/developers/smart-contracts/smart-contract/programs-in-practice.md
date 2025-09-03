# Programs in Practice

## Constant

Constants used in Qubic smart contracts should be defined with `constexpr` and follow the naming convention `[CONTRACT_NAME]_VARIABLE`.

```cpp
using namespace QPI;

constexpr sint64 MYTEST_FEE = 1000;
constexpr uint32 MYTEST_INITIAL_TICK = 19'000;

struct MYTEST2 {};

struct MYTEST : public ContractBase {};
```

## User Defined DataType

User-defined data types must be declared inside the contract struct to avoid name conflicts between different contracts.

```cpp
using namespace QPI;

struct MYTEST2 {};

struct MYTEST : public ContractBase {
  struct User {
    // ...
  };

  struct Student {
    // ...
  };
};

```

## Contract Error

Declare contract-specific errors as an `enum`

```cpp
enum ContractNameError {
	ERROR_1 = 1,
	ERROR_2,
};
```

## SELF And SELF_INDEX

-   `SELF` is your contract id (public key). Or you can generate it manually by `id(CONTRACT_INDEX, 0, 0 , 0)`.

-   `SELF_INDEX` is your contract index.

## Smart Contract Initialization

Always initialize all state variables explicitly in `INITIALIZE()` procedure.

```cpp
INITIALIZE() {
    state.a = 0;
    state.b = 1;
}
```

## String Implementation

Using `""` in smart contract is prohibited, use to represent string you can use this implementation.

[**String Implementation**](https://github.com/hackerby888/qubic-sc-examples/blob/qubic-name-service/src/contracts/QNS.h#L42)

[**String Implementation Extended**](https://github.com/hackerby888/qubic-sc-examples/blob/qubic-name-service/test/contract_qns.cpp#L22)

## Advanced Data Types in QPI

Qubic's Programming Interface (QPI) provides **high-performance, deterministic data structures** optimized for smart contract execution, including:

### HashMap (Key-Value Store)

**Example:**

```cpp
// Token balance tracking
HashMap<id, sint64, 1024> balances;
balances.set(userId, 1000);

// Fast lookup
sint64 amount;
if (balances.get(userId, amount)) {
    qpi.transfer(recipient, amount);
}
```

### BitArray (Compact Boolean Storage)

**Example:**

```cpp
// Track 256 permissions (uses only 32 bytes)
BitArray<256> userPermissions;

// Set bit at position 42 to 'true' (grant access)
userPermissions.set(42, true);

// Check permission status (returns 'bit' type)
bit hasAccess = userPermissions.get(42);

// Bulk operation: Count active permissions
uint64 activeCount = 0;
for (uint64 i = 0; i < 256; ++i) {
    if (userPermissions.get(i)) activeCount++;
}
```

### Collections (Priority Queues)

**Example:**

```cpp
// Define a task with priority
struct Task {
    id          requester;
    uint64      dueTick;
    Array<uint8, 32> data;
};

// Initialize collection (per PoV)
Collection<Task, 1024> taskQueue;  // Holds 1024 tasks max

// Add task with priority (lower = higher priority)
sint64 addTask(const id& pov, const Task& task) {
    return taskQueue.add(pov, task, task.dueTick);
}

// Process highest-priority task (lowest dueTick)
Task getNextTask(const id& pov) {
    sint64 nextIdx = taskQueue.headIndex(pov, qpi.tick());
    if (nextIdx != NULL_INDEX) {
        return taskQueue.element(nextIdx);
    }
    return Task{}; // Null task
}
```

### HashSet (Array Of Unique Elements)

**Example:**

```cpp
// Initialize HashSet with 256 slots (max 204 items at 80% load factor)
HashSet<id, 256> whitelist;

// Add addresses to whitelist
whitelist.add(user1);  // Returns true if added
whitelist.add(user2);

// Check membership (O(1) average)
if (whitelist.contains(user1)) {
    // Grant access
}

// Remove entry
whitelist.remove(user2);  // Marks for deletion
whitelist.cleanup();      // Reclaims space
```
