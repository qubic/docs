# Upgrading

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

Qubic's network evolves through regular software updates. Some updates flow through the network without interrupting ticks; others require every node to activate the new code at the same moment. Which mode applies is determined by the change itself, not by operator preference.

This page explains the two transition modes, the consensus mechanics that force the choice, and the practical rules for planning an upgrade.

## Two transition modes

Every network upgrade takes one of two forms, distinguished by whether tick numbers stay continuous across the epoch boundary.

**Seamless transition.** Tick N is the last tick of the old epoch; tick N+1 is the first tick of the new epoch. No gap. From an observer's point of view, ticks continue their monotonic sequence and the network is never off-chain.

**Coordinated cutover.** There is a gap in tick numbers between the final tick of the previous epoch and the first tick of the new epoch. The network stops, every node updates to the new binary, and ticking resumes from a network-agreed starting point.

<ThemedImage
  alt="Tick continuity — seamless vs coordinated cutover"
  sources={{
    light: useBaseUrl('/img/upgrading-tick-continuity-light.png'),
    dark:  useBaseUrl('/img/upgrading-tick-continuity-dark.png'),
  }}
/>

Seamless upgrades were introduced with epoch 102 (see [`SEAMLESS.md`](https://github.com/qubic/core/blob/main/SEAMLESS.md) in the core repository). Before that, every upgrade was a coordinated cutover.

## What determines the mode

The choice is dictated by consensus. To understand it, we need to look at what nodes actually agree on tick-by-tick.

### The tick vote

Every ~1 second (`TARGET_TICK_DURATION = 1000ms`), each of the 676 computors broadcasts a signed tick vote. For a tick to finalize, at least 451 votes (the BFT quorum, `⌈2/3 × 676⌉ + 1 = 451`) must match — **byte for byte** — on every field:

- `timestamp` — network-agreed tick timestamp
- `prevSpectrumDigest` — Merkle root of the balance tree
- `prevUniverseDigest` — Merkle root of the asset/ownership tree
- `prevComputerDigest` — Merkle root over **every active smart contract's state**
- `transactionDigest` — hash of the tick's `TickData` (transaction set)
- four salted digests (per-computor)

If two nodes compute any of these hashes differently — even if only one node ends up in the minority — that node's vote does not align with the majority, its state diverges, and it stops advancing the chain.

<ThemedImage
  alt="Tick vote structure — 5 digest fields must match byte-for-byte across ≥451 votes"
  sources={{
    light: useBaseUrl('/img/upgrading-tick-vote-light.png'),
    dark:  useBaseUrl('/img/upgrading-tick-vote-dark.png'),
  }}
/>

Detailed spec: [whitepaper §5 · Consensus Mechanism](https://qubic.org/whitepaper).

### The upgrade question, restated

Any code change that would cause old-code and new-code to compute a **different** value for any tick-vote field forces a coordinated cutover.

Same input → different hash → no alignment → no quorum → chain halts.

## When a coordinated cutover is required

Any change to the consensus mechanics needs a synchronized activation. Concrete examples:

- **A new smart contract.** Every active contract's state contributes to `prevComputerDigest`. A node running the old binary doesn't have the new contract compiled in and therefore hashes a different digest than a node running the new binary. See [whitepaper §8 · Smart Contracts](https://qubic.org/whitepaper) for the digest construction and the three-epoch activation flow (proposal → IPO → activation).
- **Changes to a protocol feature that affects state derivation.** Examples include the Outsourced Computations (OC) framework and Oracle Machines (OM) — features that change how the network derives its state.
- **Adjustments to the revenue algorithm.** Because per-computor rewards are recorded in state at `END_EPOCH`, any change to the calculation changes the resulting state hash.
- **Changes to any digest-producing algorithm** — hash functions, digest layouts, tree constructions, salt derivation.
- **Wire-protocol changes.** If the message format between nodes changes, old and new binaries can't even communicate; they'd exchange invalid packets rather than diverging digests.

Applied without synchronization, any of these split the network into two forks: nodes running the old binary agreeing among themselves, nodes running the new binary agreeing among themselves, no cross-alignment. The chain halts.

## When a seamless transition is possible

There are two paths to seamless.

### Path A — the change doesn't touch consensus

If the change modifies only components whose outputs are not part of the tick vote, it can be deployed to nodes independently. Digest computation stays identical across old and new versions.

Examples:

- RPC / API server changes
- Logging, monitoring, metrics
- Peer-discovery / gossip-layer tuning
- Mining-side improvements that don't change proof-of-useful-work outputs
- Debug tooling, operator utilities

Nodes on the old binary and the new binary continue to produce byte-identical votes for every tick.

### Path B — the change is gate-guarded

If the change *is* consensus-touching but the switch point is deterministic — a specific epoch or tick number that every node in the network knows — old and new binaries can coexist during the update rollout. Both binaries include both code paths. All nodes flip together at the switch.

Two gating primitives are available:

```c
// Epoch gate — current pattern in qubic/core for protocol switches
if (system.epoch >= 103)
    newBehavior();
else
    oldBehavior();

// Tick gate — finer granularity when a mid-epoch switch is needed
if (system.tick >= 30000000)
    newBehavior();
else
    oldBehavior();
```

The `system.epoch >= X` pattern is used throughout `src/qubic.cpp` for protocol behavior switches, including all smart-contract construction and destruction gates (see [`contractDescriptions[i].constructionEpoch`](https://github.com/qubic/core/blob/main/src/contract_core/contract_def.h)). The `system.tick >= X` pattern is used in the codebase primarily for internal scheduling (state persistence, preloading) and is available as a valid gating primitive when a finer-than-epoch switch point is required.

Both primitives share the same guarantee: `system.epoch` and `system.tick` are network-agreed values, deterministic across all nodes at every point in time. There is no ambiguity about which side of the gate the network is on.

## When neither path works

Structural changes to the underlying wire protocol, digest layout, message format, or version-negotiation logic mean old and new binaries cannot exchange valid tick votes at all. Gating doesn't help — the binaries can't communicate to reach the gate.

For these, the network coordinates a hard restart: every computor sets `START_NETWORK_FROM_SCRATCH = 1` in `public_settings.h`, the network stops at the epoch boundary, and ticking resumes at a network-agreed starting tick and timestamp (Wednesday 12:00:00.000 UTC).

## Version compatibility rule

Qubic's version scheme is `vX.Y.Z`. The compatibility rule (from [`SEAMLESS.md`](https://github.com/qubic/core/blob/main/SEAMLESS.md) in the core repository):

- **Same `X.Y`** (patch bump only) — protocol-compatible — **seamless allowed**
- **Different `X` or `Y`** (major or minor bump) — **coordinated restart required**

The version bump signals whether the change is safe to deploy piecewise. If the update is a patch (`Z` bump), operators can update their nodes at any time before the next epoch boundary and the transition will be seamless. If it's a minor or major bump, operators receive coordinated instructions and everyone sets `START_NETWORK_FROM_SCRATCH = 1` for the boundary.

Prior-tick retention: the network keeps the last 100 ticks from the previous epoch (`TICKS_TO_KEEP_FROM_PRIOR_EPOCH = 100`, in `public_settings.h`), so nodes slightly behind at the boundary can catch up without a full state resync.

## Decision framework

<ThemedImage
  alt="Upgrade decision flow — 2 questions, 3 outcomes"
  sources={{
    light: useBaseUrl('/img/upgrading-decision-flow-light.png'),
    dark:  useBaseUrl('/img/upgrading-decision-flow-dark.png'),
  }}
/>

For each upgrade, the technical team evaluates three questions in order:

1. **Does the change affect any input to the tick-vote digests?**
   → If **no**, deploy any time. Path A seamless.
2. **If yes, can the switch point be gate-guarded on a network-known value (epoch or tick)?**
   → If **yes**, deploy in advance of the switch. Path B seamless.
3. **If no** (structural change, wire-protocol change, or the gate itself changes semantics), version bump `X` or `Y` and coordinate a restart. Everyone sets `START_NETWORK_FROM_SCRATCH = 1` at the epoch boundary.

The priority is always network safety over transition smoothness. A coordinated restart is not a failure mode — it is the correct pattern when the change is deep enough that no gate can cover it.

## Practical operator implications

- **Watch the version bump.** A patch (`Z` only) means seamless. A minor or major (`Y` or `X`) means coordinated — read the release notes for the exact `START_NETWORK_FROM_SCRATCH` instructions.
- **Update ahead of the boundary for gate-guarded changes.** If the release notes reference a switch-epoch, deploy the new binary well before that epoch begins. Nodes on the new binary before the switch behave identically to nodes on the old binary; only at the switch does behavior change.
- **Don't skip version bumps.** If a release announces `X.Y+2.Z`, upgrading directly from `X.Y.Z` may miss intermediate gates. Follow the announced upgrade path.
- **Coordinated restarts are announced in advance.** They are always aligned to Wednesday 12:00 UTC epoch boundaries.

## Related documentation

- [`SEAMLESS.md`](https://github.com/qubic/core/blob/main/SEAMLESS.md) — implementation-level operator guide in `qubic/core`
- [Consensus Mechanism (whitepaper §5)](https://qubic.org/whitepaper)
- [Smart Contracts (whitepaper §8)](https://qubic.org/whitepaper)
- [Updates and Changes](../learn/updates-changes.md) — the governance process for approving updates (complements this doc, which covers the technical activation mechanics)
- [Installation](./installation.md) — bare-metal setup
- [Configuration](./configuration.md) — `public_settings.h` reference
