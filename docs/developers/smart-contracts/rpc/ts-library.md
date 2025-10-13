# TS Library

Now that your testnet RPC server is up, let's interact with your contract using the [ts-library](https://www.npmjs.com/package/@qubic-lib/qubic-ts-library). The concept is similar to `qubic-cli`: we craft the packet and send it to the node—but this time, we'll use code instead. However, a current limitation is that we still need to represent `input` and `output` as byte arrays in JavaScript and manually parse the response bytes to construct the `output`. Let’s see how this works!

## Concept

Any packet sent to the Qubic network must begin with a `RequestResponseHeader`, which describes metadata such as the packet type and its total size. Similarly, responses from a Qubic node will also start with a `RequestResponseHeader`.

The `QubicPackageBuilder` class is a helper for combining the `RequestResponseHeader` with other structures.

:::info
Each `RequestResponseHeader` must include a unique dejavu.
:::

## Calling Function

<details>
<summary>Show `getStateNumber` Contract Function</summary>

```cpp
struct getStateNumber_input
{
};

struct getStateNumber_output
{
    uint64 stateNumber;
};

PUBLIC_FUNCTION(getStateNumber)
{
    output.stateNumber = state.stateNumber;
}
```

</details>

Instead of manually crafting and sending the packet, the RPC server provides a convenient API at `/v1/querySmartContract` which allows us to make a `POST` request to invoke a function and receive a result. Let's see how to call the `getStateNumber` contract function described above.

:::info
The `input` (body) and `output` (response) of `/v1/querySmartContract` must be encoded in **base64** format.
:::

### Using RPC Server

```ts
async function main() {
  const API = `http://ip/v1/querySmartContract`;
  let responseBase64 = await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      contractIndex: 13,
      inputType: 14, // function id
      inputSize: 0,
      requestData: "", // base64 encoded input data if any
    }),
  }).then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text();
  });

  // Decode the base64 response
  // Struct output {
  //     uint64 stateNumber;
  // }

  const responseBuffer = Buffer.from(responseBase64, "base64");
  const view = new DataView(responseBuffer.buffer);
  const stateNumber = view.getBigUint64(0, true);
  console.log("State Number:", stateNumber.toString());
}

main();
```

### Directly To Node

You can also use `ts-library` to send raw contract function packets directly to the node.

<details>
 <summary>Show Code</summary>   
```ts
async function main() {
    const peerAddress = '162.120.19.25';
    const connector = new QubicConnectorNode(31841);
    if (!connector) {
        console.error('Failed to create QubicConnectorNode instance.');
        return;
    }
    connector.connect(peerAddress);
    connector.onPeerConnected = () => {
        console.log('Connected to peer:', peerAddress);

        // First craft the RequestContractFunction package
        // This is a request to the contract at index 13, function ID 14 with no input (INPUT_SIZE = 0)
        const CONTRACT_INDEX = 13;
        const FUNCTION_ID = 14;
        const INPUT_SIZE = 0;
        const request = new RequestContractFunction(
            CONTRACT_INDEX,
            FUNCTION_ID,
            INPUT_SIZE
        );

        // craft the RequestResponseHeader package
        const header = new RequestResponseHeader(
            QubicPackageType.RequestContractFunction,
            request.getPackageSize()
        );
        header.randomizeDejaVu();

        // Now combine the header and request into a single package using QubicPackageBuilder
        const builder = new QubicPackageBuilder(header.getSize());
        builder.add(header);
        builder.add(request);
        const data = builder.getData();
        connector.sendPackage(data);
        console.log(
            "Called contract function with ID",
            FUNCTION_ID,
            "on contract at index",
            CONTRACT_INDEX,
            "with input size",
            INPUT_SIZE,
            "to peer",
            peerAddress
        );
    };

    connector.onPackageReceived = (packageData) => {
        if (
            packageData.header.getType() !==
            QubicPackageType.RespondContractFunction
        ) {
            return;
        }
        let view = new DataView(packageData.payLoad.buffer);
        let statateNumber = view.getBigUint64(0, true);
        console.log('State Number: ', statateNumber.toString());
    };

}

main();

````
</details>


## Invoke Procedure

As discussed earlier, invoking a procedure is essentially sending a transaction. The `ts-library` provides classes to help build these transactions. Let’s explore how it works.

<details>
<summary>Show `setStateNumber` Contract Function</summary>

```cpp
struct setStateNumber_input
{
    uint64 stateNumber;
};

struct setStateNumber_output
{
    uint8 result;
};

PUBLIC_PROCEDURE(setStateNumber)
{
    if (input.stateNumber < state.stateNumber)
    {
        output.result = 1;
        return;
    }

    state.stateNumber = input.stateNumber;
    output.result = 0;
}
```

</details>

### Using RPC Server

```ts
async function main() {
    const BASE_URL = `http://162.120.18.27:8000/v1`;

    // Will be used to set the transaction target tick
    const getCurrentTick = async (): Promise<number> => {
        const response = await fetch(`${BASE_URL}/tick-info`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        let json = await response.json();
        return json.tickInfo.tick;
    };

    let helper = new QubicHelper();
    const seed = 'ghromhommngqxjokdlnyjkaoxmjbnwqneiikevfkxfncftudczluvcl';
    const publicKey = new PublicKey(
        (await helper.createIdPackage(seed)).publicKey
    );
    const CONTRACT_ADDRESS =
        'NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAML';
    const SetStateNumberProcedure = 15; // The procedure ID for SetStateNumber

    // Create the payload buffer
    const payloadBuffer = new Uint8Array(8);
    const view = new DataView(payloadBuffer.buffer);
    const stateNumber = 2n; // Example state number to set
    view.setBigUint64(0, stateNumber, true); // Set the state number in the payload

    // Then wrap it to DynamicPayload
    let payLoad = new DynamicPayload(payloadBuffer.length);
    payLoad.setPayload(payloadBuffer);

    // Build the transaction
    const tx = new QubicTransaction()
        .setSourcePublicKey(publicKey)
        .setDestinationPublicKey(CONTRACT_ADDRESS) // A transfer should go to the CONTRACT_ADDRESS
        .setAmount(0) // SetStateNumber does not require any fee or cost
        .setTick((await getCurrentTick()) + 10) // Set the target tick
        .setInputType(SetStateNumberProcedure)
        .setPayload(payLoad); // The payload contains the state number;

    // Sign the tx
    let txBuffer = await tx.build(seed);

    // Convert to base64
    let txBase64 = Buffer.from(txBuffer).toString('base64');
    console.log('Transaction Base64:', txBase64);

    // Then now broadcast the transaction to the network
    const API = `${BASE_URL}/broadcast-transaction`;
    let response = await fetch(API, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            encodedTransaction: txBase64,
        }),
    });

    response = await response.json();
    console.log('Transaction broadcast response:', response);
    console.log("Target tick:", tx.tick);
}

main();
````

### Directly To Node

In case the RPC server is down, you can broadcast your transaction directly to the node.

<details>
<summary>Show Code</summary>

```ts
async function main() {
  const peerAddress = "162.120.18.27";
  const BASE_URL = `http://162.120.18.27:8000/v1`;

  const getCurrentTick = async (): Promise<number> => {
    const response = await fetch(`${BASE_URL}/tick-info`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    let json = await response.json();
    return json.tickInfo.tick;
  };

  let helper = new QubicHelper();
  const seed = "ghromhommngqxjokdlnyjkaoxmjbnwqneiikevfkxfncftudczluvcl";
  const publicKey = new PublicKey(
    (await helper.createIdPackage(seed)).publicKey
  );
  const CONTRACT_ADDRESS =
    "NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAML";
  const SetStateNumberProcedure = 15; // The procedure ID for SetStateNumber

  const payloadBuffer = new Uint8Array(8);
  const view = new DataView(payloadBuffer.buffer);
  const stateNumber = 3n; // Example state number to set
  view.setBigUint64(0, stateNumber, true); // Set the state number in the payload

  let payLoad = new DynamicPayload(payloadBuffer.length);
  payLoad.setPayload(payloadBuffer);

  const tx = new QubicTransaction()
    .setSourcePublicKey(publicKey)
    .setDestinationPublicKey(CONTRACT_ADDRESS) // A transfer should go to the CONTRACT_ADDRESS
    .setAmount(0) // SetStateNumber does not require any fee or cost
    .setTick((await getCurrentTick()) + 10) // Set the target tick
    .setInputType(SetStateNumberProcedure)
    .setPayload(payLoad); // The payload contains the state number;

  let txBuffer = await tx.build(seed);
  const header = new RequestResponseHeader(
    QubicPackageType.BROADCAST_TRANSACTION,
    tx.getPackageSize()
  );
  header.randomizeDejaVu();
  const builder = new QubicPackageBuilder(header.getSize());
  builder.add(header);
  builder.addRaw(txBuffer);
  const data = builder.getData();

  let connector = new QubicConnectorNode(31841);
  connector.connect(peerAddress);
  connector.onPeerConnected = () => {
    if (connector.sendPackage(data)) {
      console.log("Transaction sent successfully to the node.");
      console.log("Target tick:", tx.tick);
    }
  };
}

main();
```

</details>

## References

For me details about `ts-libray` please see https://github.com/qubic/ts-library
