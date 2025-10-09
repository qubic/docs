---
sidebar_position: 1
---

# Overview

## Overview

Testing Qubic smart contracts is a critical step in ensuring their security, correctness, and efficiency before deployment. Due to Qubic's deterministic execution model and unique architecture, contract testing requires specialized approaches to verify:

**1. State Integrity** – Contracts must maintain consistent state across all nodes

**2. Deterministic Behavior** – Identical inputs must produce identical results

**3. Contract Efficiency** – Optimize computation to minimize QU consumption from the contract's balance

**4. Security Checks** – Prevent vulnerabilities like reentrancy or invalid state transitions

## Qubic Testing Framework

The Qubic Google Test (QGTest) framework is a specialized adaptation of Google Test (GTest) designed for testing Qubic smart contracts. Designed to simulate contract execution, validate logic, and ensure deterministic behavior without needing to run a full node or engage in live consensus.

## Recommended Workflow

### 1. Isolated Testing

```cpp
// Example unit test for a transfer function
TEST(Contract, TransferFailsWhenUnderfunded)
{
    // code
}
```

### 2. Testnet Deployment

- Use Qubic’s testnet mode to verify real-world behavior
- Monitor contract execution across multiple ticks
