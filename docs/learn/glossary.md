---
sidebar_label: 'Glossary'
---

# Glossary

The following terms are used throughout the Qubic documentation and development ecosystem.

## Aigarth
Aigarth is an AI-oriented project that will run on the Qubic network, which aims to utilize unused computational power for solving AI-related tasks. Its primary function is to run a special algorithm that allows for the evolution of solutions based on Helix logic gates. This process is transparent, with progress points available to all participants, promoting a collective push towards efficient solutions.

## Arbitrator
An entity within the Qubic ecosystem responsible for resolving disputes and protecting user interests. The [Arbitrator](/learn/arbitrator) sets parameters of the mining algorithm, publishes lists of computors every epoch, is developing the capacity to replace faulty computors, and accumulates QUBIC not received by underperforming computors. Each node operator individually selects their arbitrator by setting the corresponding ID in Qubic.cpp. The entity controlling the current arbitrator remains unknown, though rumors suggest it's operated by the development team.

## Candidate
A Candidate is a node that runs the [Computors](/learn/nodes) software but hasn't yet achieved the status of a Computor. In each epoch, up to 256 candidates can ascend to Computor status if they rank among the top 676 nodes based on their score. It's important to note that only Computors with a full week's status receive Qubic Units (QUs) as rewards for their performance. While Candidates don't earn any QUs, running as a Candidate is essential for pushing solutions to the blockchain, which is a prerequisite for becoming a Computor.

## Computor
[Computors](/learn/nodes) refer to the machines or nodes that participate in the network's consensus protocol and perform computation tasks. They are a critical component of the Qubic network, responsible for executing transactions on the Spectrum and running smart contracts.

## Computor Controlled Fund (CCF)
The Computor Controlled Fund is a community-driven funding mechanism designed to support the development and growth of the Qubic ecosystem. It is used to finance approved projects that contribute to expanding the capabilities, reach or efficiency of the Qubic network. Projects are proposed by community members and selected through a voting process. The CCF enables the quick definition of project packages and efficient allocation of budgets. The aim of the CCF is to empower the community to collaboratively decide on and prioritize the network's development directions.

## Energy
The amount of QUs per identity on the Spectrum (similar to "balance").

## Epoch
A one-week time period from Wednesday 12 UTC to Wednesday 12 UTC during which 1 trillion QUs are generated.

## Identity
Qubic's equivalent of an address.

## Miners
Miners in Qubic are essential for supporting Computors. Miners acquire problems or tasks from Computors. Upon finding a solution to these tasks for a given qubic ID, miners transmit their results back to the Computors. This continuous exchange of tasks and solutions is pivotal for determining scores for each ID during an epoch. High scores are instrumental for a Computor to retain its position amidst the top 676 Computors.

## Oracles
A feature in development for Qubic. In blockchain technology, oracles are third-party services that provide smart contracts with external information, enabling them to interact with the outside world.

## $QUBIC
QUs or QUBIC [Qubic Units](/learn/tokenomics) is the native coin and positioned as equivalent of "energy" units spent to run smart contracts and access other services in Qubic (e.g. donations to oracles). Yes, QUs can be used as money, but they are more than that. Transfers are feeless and notion of "fee" for smart contracts doesn't make much sense, because qus are destroyed, not given to computors. When one asks an oracle he "burns" QUs as a sacrifice, not as a payment, it's not even guaranteed that the oracle will answer. 

## Quorum
A quorum is the minimum number of computors necessary to conduct any sort of business. In Qubic the [Quorum](/learn/quorum) is ⅔ (or 451) of all Computors to reach consensus.

## Smart Contracts
Self-executing contracts with the terms of the agreement directly written into code. Qubic's first [smart contract](/learn/smart-contracts) was an Initial Public Offering ([IPO](/learn/ipo)) of 676 shares for a decentralized exchange (DEX) named [Qx](/learn/qx).

## Spectrum
Qubic's equivalent of a ledger. In the [Spectrum](/learn/spectrum) the energy (i.e. QUs) per Identity is stored. Qubic itself does not not keep track of transactions.

## Ticks
In the Qubic ecosystem, the tick is the interval within which the Quorum commes to an agreement on transactions and the outcome computed smart contracts. A single tick can last a very short interval of time (below 1 second).

## Useful Proof of Work (UPoW)
A novel consensus mechanism that optimizes the energy expended in mining processes by directing computational power towards valuable, real-world tasks, such as training artificial intelligence models. Unlike traditional Proof of Work systems that "waste" energy by solving abstract puzzles, [UPoW](/learn/upow) contributes to meaningful applications.


\_

Please note that Qubic is still in development, and some aspects of the system are subject to change during the development and practical testing phase. No official whitepaper is available as of yet due to this ongoing development process.
