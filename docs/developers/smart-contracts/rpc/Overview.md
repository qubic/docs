# Overview

In the [CLI Tools section](/developers/smart-contracts/cli/Overview), we learned how to interact with a Qubic node directly using `qubic-cli`. However, in a real production environment, it is unlikely that you'll communicate with a node directly. Instead, you'll typically interact through [RPC endpoints](https://docs.qubic.org/api/rpc/), which expose these operations as web (HTTP) services.

This chapter will guide you through setting up your own testnet RPC server and show you how to interact with it using the [ts-library](https://github.com/qubic/ts-library).
