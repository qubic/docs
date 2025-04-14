---
title: Qubic RPC
---
# Qubic RPC

The Qubic RPC (Remote Procedure Call) API provides a way for applications to interact with the Qubic blockchain without running a full node. It offers endpoints for querying blockchain data, submitting transactions, and interacting with smart contracts.

## Available RPC Services and Documentation
- [Qubic Live Tree](https://qubic.github.io/integration/Partners/qubic-rpc-doc.html?urls.primaryName=Qubic%20RPC%20Live%20Tree) - For real-time data access. All endpoints are mapped out here for easy reference.
- [Qubic Archive Tree](https://qubic.github.io/integration/Partners/qubic-rpc-doc.html?urls.primaryName=Qubic%20RPC%20Archive%20Tree) - Detailed API reference for historical data and past transactions. Every endpoint is documented for clarity.

## Public RPC Endpoints

| Base URL | Version/State | Use Case |
| -------- | ------- | ---- |
| https://rpc.qubic.org | V1 | Public RPC/API for general purposes. Use this in production applications. |
| https://testnet-rpc.qubic.org | V1 | Testnet RPC for development and testing |
| https://rpc-staging.qubic.org | V2 | Public RPC/API for staging (production testing) purposes. Normally only for internal testing. |

## Using RPC Endpoints

These endpoints can be accessed via HTTP requests (e.g., using `curl`, a TypeScript library, or any HTTP client). Example using `curl`:

```bash
curl https://rpc.qubic.org/v1/status
```

## Example: Smart Contract Interaction Flow

Here's how to interact with a smart contract through RPC:

:::important Base64 Encoding
When sending data (like `requestData`) in `POST` requests to endpoints such as `/v1/querySmartContract`, it **must be encoded in base64**.

Similarly, the `responseData` received from such endpoints is often encoded in base64 and **must be decoded** to get the actual data.
:::

1. **Reading Data (Function Call)**:
   ```bash
   curl -X 'POST' \
     'https://rpc.qubic.org/v1/querySmartContract' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
     "contractIndex": 1,
     "inputType": 1,
     "inputSize": 0,
     "requestData": "<BASE64_ENCODED_DATA>"
   }'
   ```
   Response: `{"responseData":"AMqaO0BCDwBAS0wA"}` (Note: The response is also encoded in base64. You will need to decode it to get the actual data.)

2. **Writing Data (Procedure Call)**:
   - Create a transaction targeting the smart contract
   - Set the appropriate function index and parameters
   - Sign the transaction with your private key
   - Broadcast it using `/v1/broadcast-transaction`

## Testing Custom Smart Contracts

When interacting with custom smart contracts:

- For custom contracts not yet deployed on mainnet, initial testing should be done through a testnet node. Refer to the [Testnet Resources](../developers/testnet-resources.md) for information on testnet nodes and faucets.
- After verifying your contract works correctly, you can integrate it with frontend applications following the patterns in the example applications.

## Best Practices

1. **Error Handling**: Always implement robust error handling for RPC calls
2. **Security**: Never expose private keys in client-side code; use proper wallet integration

For further integration details, explore the [Qubic Integration GitHub](https://qubic.github.io/integration/Partners/qubic-rpc-doc.html).

