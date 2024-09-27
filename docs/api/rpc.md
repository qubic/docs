---
title: Qubic RPC
---
# Qubic RPC

### Swagger API Documentation

For detailed information on the API, please refer to the [Qubic RPC Swagger Documentation](https://qubic.github.io/integration/Partners/qubic-rpc-doc.html?urls.primaryName=Qubic%20RPC%20Archive%20Tree).

### Public available RPC/API's


| Base Url | Version/State | Use Case |
| -------- | ------- | ---- |
| testapi.qubic.org  | V2 | Test RPC/API with the latest features. Use this in your development environment or to try out the latest features.    |
| rpc-staging.qubic.org | V2 | Public RPC/API for staging (production testing) purposes. Normally only for internal Testing. Ask us if you want to test the latest features that will be in production soon.   |
| rpc.qubic.org    | V1   | Public RPC/API for general purposes. Use this in your productive applications. |


## RPC Endpoints

### 1. Get Latest Tick
- **Method:** GET
- **Endpoint:** `/latestTick`
- **Description:** Get the current tick (block height).

### 2. Broadcast Transaction
- **Method:** POST
- **Endpoint:** `/broadcast-transaction`
- **Description:** Broadcast a transaction.

### 3. Get Approved Transactions for a Tick
- **Method:** GET
- **Endpoint:** `/ticks/{tickNumber}/approved-transactions`
- **Description:** Get a list of approved transactions for the given tick.

### 4. Get Transaction Status
- **Method:** GET
- **Endpoint:** `/tx-status/{txId}`
- **Description:** Get the status of a single transaction.

### 5. Get Tick Data
- **Method:** GET
- **Endpoint:** `/ticks/{tickNumber}/tick-data`
- **Description:** Get tick information like timestamp, epoch, included tx ids.

### 6. Get Address Balance
- **Method:** GET
- **Endpoint:** `/balances/{addressID}`
- **Description:** Get balance for specified address ID.

### 7. Get RPC Status
- **Method:** GET
- **Endpoint:** `/status`
- **Description:** Get the RPC status.

### 8. Get Chain Hash
- **Method:** GET
- **Endpoint:** `/v1/ticks/{tickNumber}/chain-hash`
- **Description:** Get the chain hash for a specific tick.

### 9. Get Quorum Tick Data
- **Method:** GET
- **Endpoint:** `/v1/ticks/{tickNumber}/quorum-tick-data`
- **Description:** Get quorum tick data for a specific tick.

### 10. Get Store Hash
- **Method:** GET
- **Endpoint:** `/v1/ticks/{tickNumber}/store-hash`
- **Description:** Get the store hash for a specific tick.

### 11. Get Transaction
- **Method:** GET
- **Endpoint:** `/v1/transactions/{txId}`
- **Description:** Get details of a specific transaction.

### 12. Get Transaction Status
- **Method:** GET
- **Endpoint:** `/v1/tx-status/{txId}`
- **Description:** Get the status of a specific transaction.

### 13. Get Transfer Transactions Per Tick
- **Method:** GET
- **Endpoint:** `/v1/identities/{identity}/transfer-transactions`
- **Description:** Get transfer transactions for a specific identity within a tick range.

### 14. Get Health Check
- **Method:** GET
- **Endpoint:** `/v1/healthcheck`
- **Description:** Get the health status of the RPC server.

### 15. Get Computors
- **Method:** GET
- **Endpoint:** `/v1/epochs/{epoch}/computors`
- **Description:** Get the list of computors for a specific epoch.

### 16. Query Smart Contract
- **Method:** POST
- **Endpoint:** `/querySmartContract`
- **Description:** Query a smart contract.

### 17. Get Tick Info
- **Method:** GET
- **Endpoint:** `/tick-info`
- **Description:** Get information about a specific tick.

### 18. Get Issued Assets
- **Method:** GET
- **Endpoint:** `/assets/{identity}/issued`
- **Description:** Get the list of assets issued by a specific identity.

### 19. Get Owned Assets
- **Method:** GET
- **Endpoint:** `/assets/{identity}/owned`
- **Description:** Get the list of assets owned by a specific identity.

### 20. Get Possessed Assets
- **Method:** GET
- **Endpoint:** `/assets/{identity}/possessed`
- **Description:** Get the list of assets possessed by a specific identity.

### 21. Get Identity Balance
- **Method:** GET
- **Endpoint:** `/balances/{id}`
- **Description:** Get the balance of a specific identity.

### 22. Get Block Height
- **Method:** GET
- **Endpoint:** `/block-height`
- **Description:** Get the current block height.

### 23. Get Latest Stats
- **Method:** GET
- **Endpoint:** `/v1/latest-stats`
- **Description:** Get the latest statistics of the RPC server. The response includes the following data:
  - `timestamp`: The current timestamp (e.g., "1724325433")
  - `circulatingSupply`: The total number of QUs in circulation (e.g., "109929085175710")
  - `activeAddresses`: The number of active addresses on the network (e.g., 477228)
  - `price`: The current price of QU in USD (e.g., 0.000001743)
  - `marketCap`: The current market capitalization in USD (e.g., "191606393")
  - `epoch`: The current epoch number (e.g., 123)
  - `currentTick`: The current tick number (e.g., 15511954)
  - `ticksInCurrentEpoch`: The number of ticks that have occurred in the current epoch (e.g., 11954)
  - `emptyTicksInCurrentEpoch`: The number of empty ticks in the current epoch (e.g., 287)
  - `epochTickQuality`: The quality of ticks in the current epoch as a percentage (e.g., 97.59913)
  - `burnedQus`: The total number of QUs that have been burned (e.g., "13070914824290")

## Interact with QX Smart Contracts using the API

For more detailed information on all available endpoints, please visit the [Qubic Swagger Documentation](https://qubic.github.io/go-qubic/swagger/index.html#/).

### QxService Endpoints
- **GET** `/v1/qx/getAssetAskOrders`
- **GET** `/v1/qx/getAssetBidOrders`
- **GET** `/v1/qx/getEntityAskOrders`
- **GET** `/v1/qx/getEntityBidOrders`
- **GET** `/v1/qx/getFees`

For interacting with these endpoints, use the base URL: `https://api.qubic.org`. For example, to get fees, you can use the following curl command: