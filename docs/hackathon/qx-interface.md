---
title: QX Interface
---

**Disclaimer:** Teams need to create a Qubic wallet on [Qubic Wallet](https://wallet.qubic.org/) and we will transfer 10 CFB so they can use the asset to test their solution. Just reach someone in the Qubic team on the hackathon to transfer the funds.

Create a user-friendly interface for QX (Qubic's decentralized exchange) similar to Uniswap. Focus on simplicity and ease of use for trading Qubic-based assets. 

# Displaying qx data

Swagger documentation for getting qx data can be found here: https://qubic.github.io/go-qubic/swagger/index.html#/QxService

## Getting asset orders

There are 2 endpoints that need to be called in order to have the orders for an **asset**:
- sell orders for the asset (ask orders)
- buy orders for the asset (bid orders)

In order to get sell orders for an asset you need to know the asset identifier which is a combination of both the asset name 
and the issuer id of that asset. 

Here are all the assets that Qubic currently has:

- CFB: CFBMEMZOIDEXQAUXYYSZIURADQLAPWPMNJXQSNVQZAHYVOPYUKKJBJUCTVJL
- QX: ::PLACEHOLDER::
- QTRY: ::PLACEHOLDER::
- RANDOM: ::PLACEHOLDER::
- MLM: ::PLACEHOLDER::
- QFT: TFUYVBXYIYBVTEMJHAJGEJOOZHJBQFVQLTBBKMEHPEVIZFXZRPEYFUWGTIWG
- QPOOL: ::PLACEHOLDER::
- QUTIL: ::PLACEHOLDER::
- QWALLET: QWALLETSGQVAGBHUCVVXWZXMBKQBPQQSHRYKZGEJWFVNUFCEDDPRMKTAUVHA


```shell
~ curl https://api.qubic.org/v1/qx/getAssetAskOrders?assetName=CFB&issuerId=CFBMEMZOIDEXQAUXYYSZIURADQLAPWPMNJXQSNVQZAHYVOPYUKKJBJUCTVJL | jq
{
  "orders": [
    {
      "entityId": "VBTBKDRJJACDRGCDPQFUDLQBSJDAJGBBZHGJYDYTABDLSJMUQWWAXDLDRDVI",
      "price": "4",
      "numberOfShares": "50999800"
    },
    {
      "entityId": "EEWCBEZNLEITWFWVEOFBLKHVXTAARMIGJNXICDIRIFDBUDGFXEYABULCFXAN",
      "price": "4",
      "numberOfShares": "10000000"
    }
  ]
}
```

Similar for buy orders:

```shell
~ curl https://api.qubic.org/v1/qx/getAssetBidOrders?assetName=CFB&issuerId=CFBMEMZOIDEXQAUXYYSZIURADQLAPWPMNJXQSNVQZAHYVOPYUKKJBJUCTVJL | jq
{
  "orders": [
    {
      "entityId": "VBTBKDRJJACDRGCDPQFUDLQBSJDAJGBBZHGJYDYTABDLSJMUQWWAXDLDRDVI",
      "price": "3",
      "numberOfShares": "2112100"
    },
    {
      "entityId": "EEWCBEZNLEITWFWVEOFBLKHVXTAARMIGJNXICDIRIFDBUDGFXEYABULCFXAN",
      "price": "3",
      "numberOfShares": "1000000"
    }
  ]
}
```

# Matching an order

If a user wants to buy an asset, he will look at the sell orders and he should submit an opposite(buy) order that will match the desired sell order.

So for example the user wants to buy the following sell order:

```json
{
  "entityId": "VBTBKDRJJACDRGCDPQFUDLQBSJDAJGBBZHGJYDYTABDLSJMUQWWAXDLDRDVI",
  "price": "4",
  "numberOfShares": "50999800"
}
```

He needs the asset identifier(asset name and issuer id) and the sell order that he wants to match(price and number of shares).
Having the information ready, you can use the js library to construct the buy transaction that will be submitted to the network:

```javascript

/*
* Example for creating a BID transaction on QX
* Buying 100 CFB tokens at 4 QU each
*/

//Api parameters
const baseURL = "https://rpc.qubic.org"
const transactionBroadcastTickOffset = 10

// Asset information
const CFBAssetIssuer = "CFBMEMZOIDEXQAUXYYSZIURADQLAPWPMNJXQSNVQZAHYVOPYUKKJBJUCTVJL"
const CFBAssetNameValue = valueOfAssetName("CFB")

// Desired price and quantity
const assetPrice = 4
const assetQuantity = 100

// Buyer information
const identity = "OURIDENTITYHERE"
const seed = "yourseedhere"


//Utility functions

//Transforms the asset name into a number used to identify the asset
function valueOfAssetName(assetName) {

    const bytes = new Uint8Array(8)
    bytes.set(new TextEncoder().encode(assetName))

    return new DataView(bytes.buffer).getInt32(0, true)
}

async function fetchLastTick(){
    const response =  await fetch(baseURL + "/v1/status", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    })

    const data = await response.json()
    return data["lastProcessedTick"]["tickNumber"]
}


function createQXOrderPayload(issuer, assetName, price, numberOfShares) {
    return new QubicTransferQXOrderPayload({
        issuer: new PublicKey(issuer),
        assetName: new Long(assetName),
        price: new Long(price),
        numberOfShares: new Long(numberOfShares),
    })
}

//Creates a transaction then signs it 
async function createQXOrderTransaction(senderId, senderSeed, targetTick, payload, actionType) {
    const transaction = new QubicTransaction()
        .setSourcePublicKey(new PublicKey(senderId))
        .setDestinationPublicKey(QubicDefinitions.QX_ADDRESS)
        .setTick(targetTick)
        .setInputSize(payload.getPackageSize())
        .setAmount(new Long(0))
        .setInputType(actionType)
        .setPayload(payload);

    if (actionType === QubicDefinitions.QX_ADD_BID_ORDER) {
        transaction.setAmount(new Long(payload.getTotalAmount()))
    }

    await transaction.build(senderSeed)

    return transaction;
}

//Encodes the signed transaction to Base64, then performs a request to the API to broadcast it
async function broadcastTransaction(transaction) {

    const encodedTransaction = transaction.encodeTransactionToBase64(transaction.getPackageData())

    return await fetch(baseURL + "/v1/broadcast-transaction",
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(
                {
                    encodedTransaction: encodedTransaction
                }
            )
        });
}

async function main() {

    //Get latest tick
    const latestTick = await fetchLastTick();

    //Assemble transaction payload
    const orderPayload = createQXOrderPayload(CFBAssetIssuer, CFBAssetNameValue, assetPrice, assetQuantity);

    //Assemble transaction
    const transaction = await createQXOrderTransaction(identity, seed, latestTick + transactionBroadcastTickOffset, orderPayload, QubicDefinitions.QX_ADD_BID_ORDER)

    //Broadcast transaction
    const res = await broadcastTransaction(transaction)
    console.log(await res.json())
}

await main()
```
> **Note:** Creating a bid (buy) order will remove the amount of funds needed to purchase the assets.  
> If the funds are unavailable, the transaction will fail and no funds will be transferred.

Similar for a user that wants to sell an asset, the same information is needed, and he should create the sell order that will match the buy order:

```javascript

/*
* Example for creating an ASK transaction on QX
* Selling 100 CFB tokens at 4 QU each
*/

//Api parameters
const baseURL = "https://rpc.qubic.org"
const transactionBroadcastTickOffset = 10

// Asset information
const CFBAssetIssuer = "CFBMEMZOIDEXQAUXYYSZIURADQLAPWPMNJXQSNVQZAHYVOPYUKKJBJUCTVJL"
const CFBAssetNameValue = valueOfAssetName("CFB")

// Desired price and quantity
const assetPrice = 4
const assetQuantity = 100

// Buyer information
const identity = "OURIDENTITYHERE"
const seed = "yourseedhere"


//Utility functions

//Transforms the asset name into a number used to identify the asset
function valueOfAssetName(assetName) {

    const bytes = new Uint8Array(8)
    bytes.set(new TextEncoder().encode(assetName))

    return new DataView(bytes.buffer).getInt32(0, true)
}

async function fetchLastTick(){
    const response =  await fetch(baseURL + "/v1/status", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    })

    const data = await response.json()
    return data["lastProcessedTick"]["tickNumber"]
}


function createQXOrderPayload(issuer, assetName, price, numberOfShares) {
    return new QubicTransferQXOrderPayload({
        issuer: new PublicKey(issuer),
        assetName: new Long(assetName),
        price: new Long(price),
        numberOfShares: new Long(numberOfShares),
    })
}

//Creates a transaction then signs it 
async function createQXOrderTransaction(senderId, senderSeed, targetTick, payload, actionType) {
    const transaction = new QubicTransaction()
        .setSourcePublicKey(new PublicKey(senderId))
        .setDestinationPublicKey(QubicDefinitions.QX_ADDRESS)
        .setTick(targetTick)
        .setInputSize(payload.getPackageSize())
        .setAmount(new Long(0))
        .setInputType(actionType)
        .setPayload(payload);

    if (actionType === QubicDefinitions.QX_ADD_ASK_ORDER) {
        transaction.setAmount(new Long(payload.getTotalAmount()))
    }

    await transaction.build(senderSeed)

    return transaction;
}

//Encodes the signed transaction to Base64, then performs a request to the API to broadcast it
async function broadcastTransaction(transaction) {

    const encodedTransaction = transaction.encodeTransactionToBase64(transaction.getPackageData())

    return await fetch(baseURL + "/v1/broadcast-transaction",
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(
                {
                    encodedTransaction: encodedTransaction
                }
            )
        });
}

async function main() {

    //Get latest tick
    const latestTick = await fetchLastTick();

    //Assemble transaction payload
    const orderPayload = createQXOrderPayload(CFBAssetIssuer, CFBAssetNameValue, assetPrice, assetQuantity);

    //Assemble transaction
    const transaction = await createQXOrderTransaction(identity, seed, latestTick + transactionBroadcastTickOffset, orderPayload, QubicDefinitions.QX_ADD_BID_ORDER)

    //Broadcast transaction
    const res = await broadcastTransaction(transaction)
    console.log(await res.json())
}

await main()
```
> **Note:** Creating an ask (sell) order, as well as canceling orders, does not cost funds.  
> Cancelling orders is done the same as in the previous example, but the order action needs to be `QX_REMOVE_ASK_ORDER` or `QX_REMOVE_BID_ORDER`, depending on which kind of order you wish to cancel.

