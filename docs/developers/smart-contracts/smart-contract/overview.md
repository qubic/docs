---
sidebar_position: 1
---

# Overview

In Qubic, smart contracts are implemented in a restricted variant of **C++** and compiled into the Qubic Core executable.

To isolate contracts, access to other contracts and Core internals is only allowed via the `QPI` (Qubic Programming Interface), the sole external dependency permitted. Using libraries is forbidden. Contracts also cannot use insecure **C++** features like pointers, low-level arrays (no bounds checking), or preprocessor directives. All memory is zero-initialized, so contracts never access uninitialized memory.

A contract has a state struct, containing all its data as member variables. The memory available to the contract is allocated statically, but extending the state will be possible between epochs through special `EXPAND` events.

**Important considerations for contract developers:**

- Contract execution incurs fees, paid from an execution fee reserve funded by QUs burned during the IPO and through ongoing burns. A contract must continue burning QUs to stay active—once the reserve is empty, it stops executing. See [Contract Execution Fees](/learn/contract-execution-fees) for details.
