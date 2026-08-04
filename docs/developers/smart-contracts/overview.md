---
title: Smart Contracts Overview
sidebar_position: 1
---

# QUBIC Smart Contract

:::tip Ready to build?
The fastest way to start developing a Qubic smart contract is the **[AIO Qubic Dev Kit](getting-started/setup-environment.md#aio-qubic-dev-kit-linux--recommended)** — one repo, Docker-based, includes Core + Faucet + Wallet + RPC. Continue with [Add Your Contract](getting-started/add-your-contract.md) once your environment is up.
:::

QUBIC smart contracts are decentralized `C++` programs that execute directly on baremetal hardware, eliminating the need for traditional operating systems or virtual machines. This low-level execution model provides high performance, low latency, and fine-grained control over computation. Unlike conventional blockchain platforms, QUBIC offers a unique architecture where contracts run closer to the hardware, ensuring deterministic and efficient execution across the network.

Each smart contract can be launched through an IPO (Initial Public Offering), a mechanism that gathers community support and allocates computing resources to the contract. This system ensures that only valuable and trusted computations receive execution time, making QUBIC smart contracts efficient, scalable, and suitable for advanced decentralized applications.

# Key Features

**1. Baremetal Execution**

Smart contracts run directly on the hardware—without an OS, VM, or container layer—allowing extremely low-level control, high-speed execution, and minimal overhead.

**2. IPO-Based Deployment (Initial Public Offering)**

Each contract must be proposed through a voting process, where the computor allocates compute resources for its execution. If the proposal is accepted, the contract will be integrated into the core code, after which the IPO process takes place. If all shares are successfully sold during the IPO, the contract will be constructed.

**3. No Virtual Machine, No Gas Model**

There is no EVM-like gas mechanism. Instead, compute resources are provisioned via IPO and scheduled execution, avoiding the need for micro-fees or instruction-based billing.

## From Code to Mainnet

Building a smart contract is only the first step. Before your contract runs on mainnet, it goes through testing, PR review, computor voting, and an IPO phase. See the complete [Smart Contract Lifecycle](lifecycle.md) for the end-to-end process from research to post-launch maintenance.
