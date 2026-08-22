# How the emission mechanism works

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

Qubic's monetary policy is not a single knob. It's a chain of protocol steps that runs at every epoch boundary. This page walks through the mechanism end-to-end, from gross emission down to the smart contract that actually removes QU from circulating supply.

If you've heard someone say "the halving" and wanted to know exactly what changes and where, this is the doc.

## Two different things called "halving"

The word is used ambiguously across chains, and Qubic's version isn't the same as Bitcoin's:

- **Bitcoin.** The block-subsidy issuance itself is cut in half. Fewer new coins per block, permanently.
- **Qubic.** The **gross emission is unchanged**. What changes is the fraction of computor revenue that gets **routed to a burn destination** instead of being paid out to the computor.

Both produce a similar directional effect on net circulating supply. The mechanism is different.

## Gross vs net emission

Every epoch (one calendar week), the protocol mints a fixed amount:

- `ISSUANCE_RATE = 1_000_000_000_000` QU — one trillion QU per epoch. Defined at compile time in `qubic/core/src/network_messages/common_def.h` and unchanged since genesis.

This is the **gross** emission. What actually enters circulating user hands is smaller, because a portion of the gross emission is burned before it reaches computors. The difference is **net** emission.

The chain has several burn paths (SC-IPO Dutch auction bids, dust-threshold burns, XMR-driven programs, and more) — the one we're documenting here is the largest and the one the "halving" adjusts.

## Mining, election, and revenue span two epochs

Before we walk through what happens inside one epoch, note that a computor's life spans two epoch boundaries. Mining is continuous — anyone can produce UPoW proofs and accumulate scores against their public key. At the end of an epoch, the top 676 pubkeys by score are seated as computors for the *next* epoch, and *those* computors are the ones who receive revenue at the end of that next epoch.

<ThemedImage
  alt="Mining, election, and revenue span two epochs"
  sources={{
    light: useBaseUrl('/img/emission-multi-epoch-light.png'),
    dark:  useBaseUrl('/img/emission-multi-epoch-dark.png'),
  }}
/>

The rest of this page zooms into *one* epoch — specifically, the end-of-epoch cascade that computes revenue, applies the routing table, and pays computors. Election happens as part of that same boundary transition; see [Upgrading](../computors/upgrading.md) for the tick-continuity mechanics.

## From gross emission to computor revenue

Inside one epoch, emission is paid out per computor through this sequence:

1. **Epoch N: work.** The 676 computors seated for epoch N produce ticks, sign votes, and process transactions. Their per-tick contribution is tracked.
2. **End of epoch N: revenue calculation.** The core computes each computor's revenue for the epoch based on their performance.
3. **End of epoch N: donation-table pass.** Before revenue reaches each computor, the routing table in the [`GQMPROP`](#the-routing-table) contract is applied sequentially (see next section). Each entry deducts a fraction of what remains.
4. **End of epoch N: distribute.** Whatever is left after the donation-table pass is paid to the computor; the residual of the epoch's ISSUANCE_RATE that wasn't consumed by computors goes to the arbitrator identity.
5. **Epoch N+1 begins.** The next epoch's computor set is seated (elected from the highest UPoW-scoring identities of epoch N), and the loop repeats.

Points 2 through 4 all happen inside `endEpoch()` in `qubic/core/src/qubic.cpp` — the per-computor revenue loop, the donation-table application, and the actual balance updates to the computor and arbitrator identities are one function call.

## The routing table

The **revenue-donation table** lives in the `GQMPROP` contract's on-chain state. Each entry is:

```
{
  destinationPublicKey  // where the routed portion goes
  millionthAmount       // fraction (in millionths — 1_000_000 = 100%)
  firstEpoch            // the first epoch this entry becomes active
}
```

The table has at most 128 entries. Entries can be added, modified, or replaced only by **quorum vote** — a computor submits a `TransferInEpoch` proposal via `GQMPROP.SetProposal(...)`, computors vote via `GQMPROP.Vote(...)`, and at the start of the next epoch `GQMPROP.BEGIN_EPOCH()` checks whether the proposal reached quorum (≥451 of 676) and majority for a non-status-quo option. If so, the entry is written into the table with the requested `millionthAmount` and `firstEpoch`.

### Sequential application

At `endEpoch()`, the routing table is applied **sequentially, per computor**. Each entry takes its `millionthAmount / 1_000_000` fraction of *what remains after previous deductions*, not of the initial revenue:

```
revenue = base * performance
for each entry in table:
    if system.epoch >= entry.firstEpoch:
        donation = revenue * entry.millionthAmount / 1_000_000
        revenue -= donation
        // donation is sent to entry.destinationPublicKey
```

This means fractions don't add — they compound. If the table has one entry at 55% and another at 8%, the second doesn't take 8% of gross, it takes 8% of the 45% that remains.

<ThemedImage
  alt="Sequential deduction — the routing table applied per computor"
  sources={{
    light: useBaseUrl('/img/emission-sequential-deduction-light.png'),
    dark:  useBaseUrl('/img/emission-sequential-deduction-dark.png'),
  }}
/>

### Auto-cleanup at BEGIN_EPOCH

When an entry with a future `firstEpoch` becomes active, any older entry with the same `destinationPublicKey` is automatically removed by `_CleanupRevenueDonation` in `GQMPROP.BEGIN_EPOCH()`. No manual removal step is needed.

### "Halving," restated

A "halving" in Qubic is just a quorum-approved entry — same `destinationPublicKey` as the previous burn-destination entry, higher `millionthAmount`, some future `firstEpoch`. When that epoch begins, the higher rate takes effect and the old entry auto-cleans.

You can inspect the current table live — see [Inspect network state](./inspect-network-state.md#worked-example--the-revenue-donation-table) for CLI, GUI, RPC, and SDK examples.

## SWATCH — the Emission SC

The routing table sends fractions of computor revenue *somewhere*. For the burn-share entry, that somewhere is the smart contract **SWATCH** (contract index 7) — the **Supply Watcher** / Emission SC.

SWATCH was created by [an approved 2024 proposal](https://qubic.org/blog-detail/the-new-emission-model-proposal-with-80-supply-cut) as an infrastructure contract:

> *"To be able to burn Qubic according to the proposed emission schedule we propose to create the Emission Smart Contract. This SC will be responsible to burn the Qubic according to Emission schedule, the Supply Watcher. Computors or any other individual can donate/send Qubic to this SC. The SC will burn them. This is an infrastructure SC and will NOT generate any dividend for shareholders."*

The proposal outlined two phases:

- **Phase 1** — SC burns everything sent to it.
- **Phase 2** — SC burns everything sent to it **while taking existing ecosystem burns into account**. This is where the "Supply Watcher" name earns itself.

## What SWATCH does today

The current SWATCH implementation lives in `qubic/core/src/contracts/SupplyWatcher.h` — approximately 65 lines. It has **one hook: `BEGIN_EPOCH`**, no user functions, no state variables of its own.

At each epoch boundary, SWATCH:

1. **Reads its own balance** — QU routed to it during the previous epoch via the donation-table pass.
2. **Reads the fee reserves** of three contracts: `GQMPROP` (index 6), `SWATCH` itself (index 7), and `CCF` (index 8), via `qpi.queryFeeReserve()`.
3. **Computes a target** — the average of those reserves + its own balance, split across three buckets, excluding buckets that are already above target.
4. **Distributes** — calls `qpi.burn(amount, contractIndex)` to top up any under-target reserves.
5. **Burns the remainder** — any balance still remaining after the top-ups is split evenly and burned via the same `qpi.burn()` primitive.

### Contract fee reserves are burn destinations

The crucial mental-model correction: **QU sent to a contract fee reserve are burned, not held**. `contractFeeReserves[]` is not a spendable balance the contract can transfer elsewhere. It is an accounting slot for the contract's own execution costs — decremented as the contract runs code (execution fees), never sent to a user identity.

Fee-reserve top-ups and the remainder's `qpi.burn()` call have the **same effect on circulating supply** — both remove QU from user hands permanently.

The reason SWATCH does both is efficiency: the same balance-inspection pass that decides how much to route to reserves also decides what's left over for the remainder burn. One BEGIN_EPOCH hook does both jobs.

<ThemedImage
  alt="SWATCH — what runs at every BEGIN_EPOCH"
  sources={{
    light: useBaseUrl('/img/emission-swatch-begin-epoch-light.png'),
    dark:  useBaseUrl('/img/emission-swatch-begin-epoch-dark.png'),
  }}
/>

## Phase 2 — Supply Watch

The Phase 2 behavior from the same 2024 proposal is where the name literally applies:

> *"SC will burn everything sent to it while taking existing ecosystem burns into account. Supply Watcher."*

The intent is adaptive burn control. Ecosystem-level burns already happen outside SWATCH — SC-IPO Dutch auction bids are burned during `finishIPOs()` each epoch; the dust-threshold rules in `qubic/core/src/spectrum/spectrum.h` burn small balances when the spectrum fills past 75%; time-limited programs (like the 2025 XMR-driven program that burned ~672B QU) contribute periodically. In Phase 2, SWATCH would read those contributions and **shrink its own burn accordingly** so the network's total burn per epoch stays on the emission schedule.

Same emission-schedule target. Adaptive per-epoch contribution.

<ThemedImage
  alt="Phase 2 Supply Watch — adaptive burn contribution"
  sources={{
    light: useBaseUrl('/img/emission-supply-watch-phase2-light.png'),
    dark:  useBaseUrl('/img/emission-supply-watch-phase2-dark.png'),
  }}
/>

## How to verify the current state

Every part of this mechanism is inspectable live. See the worked example in [Inspect network state](./inspect-network-state.md#worked-example--the-revenue-donation-table) for step-by-step how to query the current revenue-donation table via:

- `qubic-cli -gqmpropgetrevdonation`
- Qubic.Net Toolkit → Governance → Revenue tab
- HTTP RPC `POST /v1/querySmartContract`
- The TypeScript SDK helper `generalQuorumProposalGetRevenueDonation()`
- The .NET SDK `QuerySmartContractAsync<GetRevenueDonationInput, GetRevenueDonationOutput>()`

The same principle applies to inspecting SWATCH's balance, individual fee reserves, or any other on-chain state — the network exposes all of it; the tools just present it differently.

## Sources

- [`qubic/core`](https://github.com/qubic/core) — the codebase:
  - `src/network_messages/common_def.h` — `ISSUANCE_RATE`
  - `src/qubic.cpp` — `endEpoch()`, per-computor revenue loop, donation-table application
  - `src/contracts/GeneralQuorumProposal.h` — `revenueDonation` table + vote flow + `_CleanupRevenueDonation`
  - `src/contracts/SupplyWatcher.h` — the SWATCH SC itself
  - `src/qpi/impl/qpi_spectrum_impl.h` — `qpi.burn()` implementation
- [Whitepaper §14 · Governance](https://qubic.org/whitepaper) — GQMPROP overview
- [The approved proposal (2024): *The new emission model — 80% supply cut*](https://qubic.org/blog-detail/the-new-emission-model-proposal-with-80-supply-cut) — the origin of SWATCH and Phase 1 / Phase 2 design intent

## Related documentation

- [Inspect network state](./inspect-network-state.md) — CLI / GUI / RPC / SDK examples for querying the routing table and other on-chain state
- [Tokenomics](./tokenomics.md) — overview of Qubic's monetary policy
- [Governance](./governance.md) — how quorum proposals work at the protocol level
- [Upgrading](../computors/upgrading.md) — how the network transitions between epochs
