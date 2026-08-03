---
title: Typescript Libraries
---

# Typescript Libraries

Two TypeScript options exist. **Start with [qubic-typescript](#qubic-typescript-sdk)** — it covers everything the older [Qubic TypeScript Library](#qubic-typescript-library) does (identity and crypto helpers, transaction building, and direct TCP access to a node) and adds an RPC gateway client, a [Bob](https://github.com/qubic/core-bob) live-node client, typed contract wrappers, event decoding, and React hooks. It's split into focused packages, so you install only what you need.

The Qubic TypeScript Library is still worth reaching for in two cases:

- You're maintaining a project already built on it — it's stable and widely used.
- You need the raw node protocol **from a browser**, which it reaches through qubic.li's WebSocket bridge. qubic-typescript's `@qubic.org/tcp` uses Node's `net` module, so it runs on Node and Bun but not in the browser.

## qubic-typescript (SDK)

[qubic-typescript](https://github.com/qubic/qubic-typescript) is a modular TypeScript SDK, split into focused packages for crypto, transaction building, RPC, ABI codec, live node subscriptions, and React integration. It is built for [Bun](https://bun.com) and works with Node.js.

:::note
qubic-typescript is in **public beta** — core APIs are stable and in production use, but the public surface has not frozen yet. Pin to an exact version and check the changelog when upgrading.
:::

For the package list, install instructions, dependency graph, and end-to-end examples, see the [qubic-typescript README](https://github.com/qubic/qubic-typescript#readme). For frontend work specifically, the [`@qubic.org/react`](https://github.com/qubic/qubic-typescript/tree/main/packages/react) package provides hooks and wallet providers out of the box.

## Qubic TypeScript Library

The [Qubic TypeScript Library](https://github.com/qubic/ts-library) is the earlier single-package library for interacting with the Qubic network from JavaScript/TypeScript, covering identities, node connections, balances, transactions, and smart contract interaction. Its companion [Qubic Vault TypeScript Library](https://github.com/qubic/ts-vault-library) handles encrypted identity storage.

For installation and usage, see the [ts-library README](https://github.com/qubic/ts-library#readme) and the [ts-vault-library README](https://github.com/qubic/ts-vault-library#readme). The [HM25 frontend example](https://github.com/icyblob/hm25-frontend) shows both in a real application.
