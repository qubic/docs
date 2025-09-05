---
title: Ticks and Concurrency
---

# Ticks and Concurrency

## 1. Ticks vs Blocks

**Different paradigm**: Qubic does NOT use blocks, it uses "ticks"

Unlike traditional blockchains where transactions are grouped into blocks that are created every few minutes, Qubic operates on a fundamentally different architecture. The core unit of time and consensus is called a "tick."

- **Tick definition**: A complete network state snapshot that occurs every ~0.2-5 seconds, containing all validated transactions and their effects for that specific moment in time
- **Instant finality**: Once a tick is processed and accepted by the quorum of 676 Computors, transactions within it are immutably final. There is no concept of "confirmations" like in Bitcoin - the transaction either succeeded in that exact tick or it didn't
- **No direct linking**: Unlike blockchain blocks that contain cryptographic hashes linking them to previous blocks, ticks are independent snapshots. Each tick stands alone and doesn't reference previous ticks through hash chains
- **Automatic pruning**: At the end of each epoch (exactly 7 days), all historical transaction data is completely deleted from the network. Only the final account balances and essential state information survive into the next epoch. This radical approach eliminates blockchain bloat entirely

## 2. Tick Offset - Temporal Programming

**Critical concept**: Transactions must be scheduled for future execution

One of the most important concepts to understand in Qubic is that you cannot send a transaction for immediate execution. Instead, you must schedule transactions to execute at a specific future tick. This is fundamentally different from traditional blockchains where you submit a transaction and wait for miners to include it in the next available block.

```
Time flow:
Current Tick (N) → Offset (+10) → Target Tick (N+10) → Execution
```

![Time Flow](/static/img/time_flow.png)

**Why this architecture exists**:

- **Performance optimization**: By knowing exactly when transactions will execute, the network can optimize processing and achieve much higher throughput
- **Deterministic execution**: This prevents race conditions and makes the network behavior completely predictable
- **Resource planning**: Computors can prepare for the computational load of upcoming ticks

**Architectural implications**:

- **No mempool**: Because transactions are scheduled for specific ticks, there's no need for a traditional mempool where transactions wait to be processed. Either your transaction makes it into its designated tick or it's lost forever
- **Deterministic execution**: You must specify exactly WHEN your transaction will execute (the target tick number), not just submit it and hope for the best
- **Time window planning**: You need a minimum of 3 ticks offset to ensure network propagation, though most applications use 10+ ticks for safety
- **Single opportunity**: If the target tick passes and your transaction wasn't included (due to network issues, invalid signature, etc.), the transaction is irreversibly lost. There's no retry mechanism - you must create and send a new transaction

## 3. Concurrency Restriction

**Fundamental limitation**: An identifier (ID) can only have ONE pending transaction simultaneously

This is perhaps the most surprising limitation for developers coming from other blockchain platforms. In Qubic, each identity (public key) can only have one pending transaction at any given time. This restriction exists for very specific technical reasons related to how the network maintains state consistency.

```
ID State Example:
- Transaction A scheduled for tick N+5 (pending)
- Transaction B sent for tick N+7 (new)
- Result: Transaction A is automatically replaced by Transaction B
```

![Id State Example](/static/img/id_state.png)

**Why this limitation exists**:

- **State consistency**: The network needs to know the exact sequence of operations for each identity to maintain consistent balances and prevent double-spending
- **Performance optimization**: This simplifies the consensus mechanism and allows for faster processing
- **Deterministic behavior**: It eliminates race conditions between multiple pending transactions from the same identity

**Practical implications**:

- **Transaction replacement**: If you send a new transaction while another is pending, the old one is automatically discarded
- **Timing coordination**: You must carefully plan the timing of multiple operations from the same identity
- **No batching**: You cannot send multiple transactions simultaneously from the same identity

**Mitigation strategies**:

- **Sequential timing**: Space out transactions to different future ticks (e.g., tick N+5, N+6, N+7)
- **Temporary identities**: Create additional key pairs for operations that need to happen in parallel
- **Application-level queuing**: Implement transaction queues in your application logic to manage multiple operations
- **State checking**: Always verify the current pending transaction before sending a new one
