---
sidebar_label: 'Tokenomics'
---

# Qubic Tokenomics

The utility (or coin) driving the Qubic ecosystem is not a mere currency but an 'energy' unit. These units, known as $QUBIC, serve as the fuel for executing smart contracts and accessing other services on the Qubic platform. Unlike traditional monetary units, $QUBIC is burned when used, which is a fundamental concept in understanding the unique tokenomics of Qubic.

## $QUBIC
$QUBIC acts as a measurement of computational 'energy' spent on the Qubic platform. Whether it's running smart contracts or seeking data from oracles, the consumption of $QUBIC is the bedrock of transactions within the system. It's vital to note that $QUBIC, while having a value, is not 'paid' to the system entities ([Computors](/learn/nodes)). Instead, it is 'burned' or permanently removed from circulation, contributing to a balance between inflation and deflation in the Qubic economy.

:::info
The Qubic network utilizes $QUBIC (and not $QU) as its official financial ticker. 
:::

## Epoch and QU Generation
Each epoch in the Qubic network spans seven days and produces 1 trillion $QUBIC. These units are allocated to [Computors](/learn/nodes), the Computor Controlled Fund (CCF), QEarn, and burns. In scenarios of maximum efficiency, a Computor can potentially receive a revenue equivalent to 1 trillion $QUBIC divided by 676 (i.e. 1.479 billion $QUBIC). The distribution model encourages efficiency; Computors operating at suboptimal levels see reduced revenue.

## Max Supply and Emission Schedule
The circulating supply is capped at 200 trillion $QUBIC, reduced from the original 1000 trillion via [community vote](https://app.qubic.li/public/proposal/81ca1427-2ebc-4e78-a662-25a643f48292).

To reach this cap, Qubic implements a halving schedule that reduces net emissions by ~50% each halving (exact rates determined by quorum before each halving):

| Epochs | Net Emissions per Epoch |
|--------|------------------------|
| 0-126 | 1 trillion $QUBIC |
| 127-174 | 850 billion $QUBIC |
| 175-226 | 450 billion $QUBIC |
| 227-278 | ~240 billion $QUBIC |
| 279-330 | ~125 billion $QUBIC |
| 331-382 | ~65 billion $QUBIC |
| 383-434 | ~35 billion $QUBIC |
| 435-486 | ~20 billion $QUBIC |
| 487-538 | ~10 billion $QUBIC |
| 539+ | ~5 billion $QUBIC |

The first halving occurred at **Epoch 175** (August 2025), reducing net emissions from 850B to 450B per epoch. The Supply Watcher Smart Contract dynamically adjusts emissions based on real-time supply data.

## Transfers and Fees
Qubic stands apart from traditional systems with its approach to transfers and fees. Transfers within the Qubic network are **feeless**, contributing to the efficiency and user-friendly nature of the platform. Furthermore, 'fees' associated with executing smart contracts are not fees in the traditional sense. This $QUBIC is burned and not given to Computors, further reinforcing the concept of $QUBIC as 'energy' rather than money.

## The Role of Computors
[Computors](/learn/nodes) in the Qubic system play an instrumental role in maintaining its economic balance. They perform tasks assigned by the Arbitrator and vote by [Quorum](/learn/quorum) to determine the size of the commission for executing smart contracts. Interestingly, this commission does not become the Computors' income. Instead, it is burned, adjusting the inflation or deflation of $QUBIC in the ecosystem.

## The Arbitrator
The [Arbitrator](/learn/arbitrator) oversees the assignment of AI training tasks in Qubic but does not exert influence over smart contract execution, voting procedures, or $QUBIC distribution. This segregation of roles aids in maintaining the decentralized nature of the platform. However, the Arbitrator also plays a crucial role in cases of disputes or challenges within the network, providing a balanced and fair resolution. As such, the Arbitrator contributes to maintaining the overall stability and order of the Qubic ecosystem.

## Smart Contracts   
Execution of [smart contracts](/learn/smart-contracts) on Qubic typically requires a commission, unlike many other crypto platforms. However, this commission does not go into the pockets of the Computors, but rather it is burned. The size of the commission is determined through a quorum vote by the Computors, effectively creating a mechanism for automatic adjustment of inflation or deflation.

<details>
  <summary>Burn Mechanism during IPO</summary>
  <div>
    <p>
    Every new smart contract on Qubic requires an Initial Public Offering (IPO). This is not just a fundraising exercise but also a mechanism to control the QU supply. All $QUBIC spent during the IPO's Dutch auction will be permanently burned, ensuring a continuous reduction in the active supply of $QUBIC over time.
    </p>
  </div>
</details>

:::info
While $QUBIC can be seen as the native coin, [Qx](/learn/qx) shares are the first ever tokens deployed on the Qubic ecosystem.
:::

In essence, $QUBIC serves as the lifeblood of the Qubic network, driving its operations, incentivizing efficiency, and maintaining a balance in the tokenomics through a system of rewards and burns. The unique role of $QUBIC within the network design underlines the adaptive, efficient, and democratic nature of the Qubic platform.