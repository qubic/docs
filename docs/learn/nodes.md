---
sidebar_label: 'Node Types'
---

# Node Types in the Qubic Network

Within the Qubic ecosystem, two primary node types work in tandem to support its decentralised infrastructure - the Computors and the miners. These entities shoulder unique responsibilities and ensure the efficient functioning of the network.

<details>
  <summary>Computors vs. Miners in a Nutshell</summary>
  <div>
    <p>
    Traditional blockchains use miners to validate and add transactions to the blockchain. They compete for rewards in the form of cryptocurrency. Qubic, however, pivots to Computors that execute varied tasks and receive rewards in QUBIC based on overall participation. This distinction, including their reward mechanisms and roles, sets Computors apart from traditional miners, marking a shift in how decentralised systems might operate in the future.
    </p>
  </div>
</details>

## Computors

A Computor (validator) in the Qubic ecosystem is a specialised node who execute tasks, ranging from running smart contracts to facilitating transactions on the spectrum. Unlike traditional blockchain systems where miners verify and add transactions, Computors in the Qubic ecosystem bear a broader scope of duties. They are instrumental in executing tasks, participating in decentralised quorum-based decision making and maintaining the tokenomic equilibrium of the network.

**Key Features**:
- Role in maintaining and ensuring network's decentralised nature.
- Allocation of a portion of newly minted QUBIC each epoch for their overall network participation.
- Involvement in essential network voting and decision-making processes.

**Limitation**: There is a fixed upper limit of 676 Computors operating in the Qubic network at any given time, ensuring optimal performance and streamlined decision-making. A weekly score ranking based on solutions deliverd by their miners determines the top 451 performing Computors, who maintain their status, while the remaining 225 spots are filled from the pool of candidates and lower-ranking Computors each epoch.

:::tip
**Challenges of Running a Computor on Qubic:**

- Operates on bare metal, requiring UEFI control.
- Regular compilation of qubic.cpp every epoch.
- Continuous system updates.
- Need for backup systems to ensure consistent ticking.
- Competition: Must outperform candidates with enough mining power assigned to thei IDs to retain spot.

Running a Computor demands technical expertise and constant vigilance. Ensure you're prepared for these challenges if considering operating as one!
:::

## Miners

**Miners** in the Qubic ecosystem differ from their counterparts in traditional blockchain networks. Instead of competing to verify and add transactions to a blockchain, miners on Qubic work on specific computational problems or tasks assigned to them by Computors. Once they find a solution, they relay it back to the respective Computor. This interaction not only assists in verifying the integrity of the tasks but also aids in the overall processing and validation of actions within the network.

**Key Features**:
- Receive computational problems or tasks (represented by IDs) from Computors.
- Upon successful problem-solving, relay solutions back to Computors, contributing to their score.
- Integral to Qubic's innovative system, where the emphasis is not solely on transaction verification but on overall task execution.

**Potential**: The Qubic network allows for a theoretically unlimited number of miners, promoting widespread participation and ensuring robust computational power backing the system.

:::info
**Why Become a Miner?**

It's crucial to note that only Computors receive weekly payments from the Qubic protocol. However, to maintain their position among the 676 Computors, they must accumulate sufficient solutions each epoch through their associated miners. Consequently, it's inevitable that every Computor will eventually need to cultivate a robust mining pool around them and provide incentives via pool payouts.

Working as a miner is easier than working as a Computor and there are public [pools](/learn/pool) available.
:::



It's essential for any participant or observer in the Qubic network to understand this fundamental distinction between miners and Computors. As we progress into this new era of Qubic, the roles and responsibilities of both will undoubtedly become increasingly important.

## Node Implementations

Alongside the Computor/miner roles above, Qubic has several node implementations, each built for a different purpose. See each repository for full requirements and setup.

| Implementation | What it's for | Computor? | Repository |
| -------------- | ------------- | --------- | ---------- |
| **Core (Full node)** | The full node, run on bare metal with UEFI. This is the software you run to operate a [Computor](#computors) and take part in mainnet consensus. | ✅ Yes | [qubic/core](https://github.com/qubic/core) |
| **Core Lite** | The lite version of Core that runs on a normal OS without UEFI. Supports a self-contained local testnet and mainnet (beta), and ships with a built-in RPC API and block explorer — handy for developing and testing smart contracts or running a lightweight node. | ❌ No | [qubic/core-lite](https://github.com/qubic/core-lite) |
| **Bob** | An indexer/full node that syncs and verifies the network — reconstructing the Spectrum and Universe from logging events each tick — and serves it over a JSON-RPC 2.0 and REST API. Run it to power dApps, exchanges, explorers, and other products that read from or interact with the network without being a Computor. | ❌ No | [qubic/core-bob](https://github.com/qubic/core-bob) |
