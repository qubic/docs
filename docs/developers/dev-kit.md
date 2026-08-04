---
title: AIO Qubic Dev Kit
---

# AIO Qubic Dev Kit

The [**AIO Qubic Dev Kit**](https://github.com/qubic/aio-qubic-dev-kit) is the recommended tool for setting up a local Qubic development environment. Clone one repo, run `docker compose up`, and you get Core + Faucet + Wallet + RPC on localhost.

:::info Replaces the older Qubic Dev Kit
The earlier [`qubic/qubic-dev-kit`](https://github.com/qubic/qubic-dev-kit) — built for Hackathon Madrid 2025 — was **archived by the maintainers on 2026-07-22**. Its README now redirects to AIO. If you're following an older guide that pointed at it, use AIO instead.
:::

## What's in the box

- **Core** — local Qubic node
- **Faucet** — funds test identities on demand
- **Wallet** — user-side interactions with your contract
- **RPC** — the same API surface your contract will hit in production

Everything you need to build, deploy, and iterate on a smart contract locally — without touching mainnet.

## Requirements

This is a real dev environment, not a laptop toy:

- **Linux x86-64 with AVX2** — Ubuntu 24.04 recommended
- **≥24 GB RAM** — ≥32 GB for the full stack with the explorer
- **8+ CPU cores** for the full stack
- **~25–50 GB/day disk writes** at the default 1 s tick rate — provision generous disk headroom
- **Tools:** `docker.io`, `docker-compose-v2`, `git`, `python3`, `make`, `g++`, `unzip`

Not on Linux? Spin up a dev VPS (Hetzner / Contabo / Vultr / etc.) meeting the specs above. macOS and Windows are not supported for the AIO path — see the [Visual Studio alternate](smart-contracts/getting-started/setup-environment.md#visual-studio-windows--alternate) for the IDE workflow.

## Get started

```bash
sudo apt install -y docker.io docker-compose-v2 git python3 make g++ unzip
git clone https://github.com/qubic/aio-qubic-dev-kit
cd aio-qubic-dev-kit
# then follow the repo README for the current start command
```

Full step-by-step: **[Getting Started → Setup Environment](smart-contracts/getting-started/setup-environment.md#aio-qubic-dev-kit-linux--recommended)**.

## Support

Questions or setup issues? Reach out in the `#dev` channel on our Discord — the QCT team can help.

## Next steps

Once your environment is up:

1. **Learn contract structure** — [Smart Contract Overview](smart-contracts/overview.md)
2. **Walk through a full example** — [Getting Started Tutorial](smart-contracts/getting-started/setup-environment.md)
3. **Understand the QPI** — [Qubic Programming Interface](qpi.md)
4. **Study working contracts** — [Smart Contract Examples](smart-contracts/sc-by-examples/assets-and-shares.md)
