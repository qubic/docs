---
title: How Actually It Works
sidebar_position: 2
---

# Introduction

As mentioned earlier, Qubic smart contracts run directly on bare metal—no virtual machine involved. But how does it actually work? Let’s explore.

## How It Works

In Qubic, a smart contract is simply a C++ class with methods. The state of your contract is stored in the members of the smart contract class instance.

## Functions and Procedures

- **Procedure:** If a method modifies the members of the smart contract instance, it’s called a **Procedure**.
- **Function:** If a method only reads member variables without modifying them, it’s called a **Function**.

## Interacting with Smart Contracts in Qubic

- **Function:** Invoked via TCP messages. You send a message to a node requesting it to call a specific function, and the node immediately returns the response.
- **Procedure:** Invoked via transactions. Since it modifies the contract state, all nodes must execute it and update the state. The transaction specifies the contract address, the **procedure** to call, and its **parameters** (encoded in `inputHex`).
