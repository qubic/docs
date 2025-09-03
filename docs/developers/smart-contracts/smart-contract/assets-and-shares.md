---
sidebar_position: 9
---

# Assets And Shares

[**Example Source Code**](/sc-by-examples/assets-and-shares)

Asset management rights can be transferred to other contracts through `qpi.releaseShares()` or `qpi.acquireShares()`, for example, if an asset has been issued using QX but an owner of some if its shares wants to trade them using a different exchange (not QX), the management rights of these shares need to be transferred to the other contract first. Shares that are managed by QX can be released to another contract (transferring rights to manage ownership and possession) by invoking the QX user procedure `TransferShareManagementRights` (with owner/possessor as invocator). QX rejects all attempts (`qpi.acquireShares()`) of other contracts to acquire rights from QX.

## Management rights transfer

There are two ways of transferring asset management rights:

- The contract already having management rights releases them to another contract by calling `qpi.releaseShares(`).

- The contract needing management rights acquires them from the contract having the rights by calling `qpi.acquireShares()`.

### Transferring rights with `qpi.releaseShares()`

Let's assume contract A has management rights of shares and wants to transfer them to contract B.
Contract A can try to do this by calling `qpi.releaseShares()`.
In this call, the following happens:

![qpi.releaseShares()](/img/releaseShares.png)

After checking the inputs passed to `qpi.releaseShares()` by contract A, the system calls `PRE_ACQUIRE_SHARES()` of contract B to (1) query if it is willing to acquire the management rights and (2) query the fee that A needs to pay to B for the rights transfer.

An instance of the following struct is passed to the system procedure `PRE_ACQUIRE_SHARES()` of contract B as `input`:

```cpp
struct PreManagementRightsTransfer_input
{
    Asset asset;
    id owner;
    id possessor;
    sint64 numberOfShares;
    sint64 offeredFee;
    uint16 otherContractIndex;
};
```

An instance of the following struct is passed to the system procedure `PRE_ACQUIRE_SHARES()` of contract B as `output`:

```cpp
struct PreManagementRightsTransfer_output
{
    bool allowTransfer;
    sint64 requestedFee;
};
```

By default, all of `output` is set to zero, that is, `allowTransfer = false`.
Thus, if `PRE_ACQUIRE_SHARES()` is not defined or empty, all transfers are rejected.
Set `output.allowTransfer = true` in order to accept the rights transfer.

If `allowTransfer` is `false` or `requestedFee > offeredFee`, the transfer is canceled.
Otherwise, the `requestedFee` is transferred from contract A to B, followed by the transfer of the management rights from contract A to B.

Finally, the system procedure `POST_ACQUIRE_SHARES()` is called in contract B, passing an instance of the following struct as `input`:

```cpp
struct PostManagementRightsTransfer_input
{
    Asset asset;
    id owner;
    id possessor;
    sint64 numberOfShares;
    sint64 receivedFee;
    uint16 otherContractIndex;
};
```

The output of `POST_ACQUIRE_SHARES()` is empty (`NoData`).

Calling `qpi.releaseShares()` and `qpi.acquireShares()` is not permitted in the system procedures `PRE_ACQUIRE_SHARES()` and `POST_ACQUIRE_SHARES()`, that is, they will return with an error in such a context.

The function `qpi.releaseShares()` has the following parameters and return value:

```cpp
sint64 releaseShares(
    const Asset& asset,
    const id& owner,
    const id& possessor,
    sint64 numberOfShares,
    uint16 destinationOwnershipManagingContractIndex,
    uint16 destinationPossessionManagingContractIndex,
    sint64 offeredTransferFee
);
```

On success, it returns the payed fee, which is >= 0.
If `offeredTransferFee` or the contract balance is not sufficient, it returns `-requestedFee`.
In case of another error, it returns `INVALID_AMOUNT` (which is a negative number of large amount).

For more details, refer to the code of `qpi.releaseShares()` in `src/contract_core/qpi_asset_impl.h`.

### Transferring rights with `qpi.acquireShares()`

Let's assume contract A has management rights of shares and contract B wants to get them.
Contract B can try to do this by calling `qpi.acquireShares()`.
In this call, the following happens:

![qpi.acquireShares()](/img/acquireShares.png "qpi.acquireShares()")

After checking the inputs passed to `qpi.acquireShares()` by contract B, the system calls `PRE_RELEASE_SHARES()` of contract A to (1) query if it is willing to release the management rights and (2) query the fee that B needs to pay to A for the rights transfer.

An instance of the following struct is passed to the system procedure `PRE_RELEASE_SHARES()` of contract A as `input`:

```cpp
struct PreManagementRightsTransfer_input
{
    Asset asset;
    id owner;
    id possessor;
    sint64 numberOfShares;
    sint64 offeredFee;
    uint16 otherContractIndex;
};
```

An instance of the following struct is passed to the system procedure `PRE_RELEASE_SHARES()` of contract A as `output`:

```cpp
struct PreManagementRightsTransfer_output
{
    bool allowTransfer;
    sint64 requestedFee;
};
```

By default, all of `output` is set to zero, that is, `allowTransfer = false`.
Thus, if `PRE_RELEASE_SHARES()` is not defined or empty, all transfers are rejected.
Set `output.allowTransfer = true` in order to accept the rights transfer.

If `allowTransfer` is `false` or `requestedFee > offeredFee`, the transfer is canceled.
Otherwise, the `requestedFee` is transferred from contract B to A, followed by the transfer of the management rights from contract A to B.

Finally, the system procedure `POST_RELEASE_SHARES()` is called in contract A, passing an instance of the following struct as `input`:

```cpp
struct PostManagementRightsTransfer_input
{
    Asset asset;
    id owner;
    id possessor;
    sint64 numberOfShares;
    sint64 receivedFee;
    uint16 otherContractIndex;
};
```

The output of `POST_RELEASE_SHARES()` is empty (`NoData`).

Calling `qpi.releaseShares()` and `qpi.acquireShares()` is not permitted in the system procedures `PRE_RELEASE_SHARES()` and `POST_RELEASE_SHARES()`, that is, they will return with an error in such a context.

The function `qpi.acquireShares()` has the following parameters and return value:

```cpp
sint64 acquireShares(
    const Asset& asset,
    const id& owner,
    const id& possessor,
    sint64 numberOfShares,
    uint16 sourceOwnershipManagingContractIndex,
    uint16 sourcePossessionManagingContractIndex,
    sint64 offeredTransferFee
);
```

On success, it returns the payed fee, which is >= 0.
If `offeredTransferFee` or the contract balance is not sufficient, it returns `-requestedFee`.
In case of another error, it returns `INVALID_AMOUNT` (which is a negative number of large amount).

For more details, refer to the code of `qpi.acquireShares()` in `src/contract_core/qpi_asset_impl.h`.

#### Notes and recommendations

By default, management rights of shares can be transferred without the agreement of the owner/possessor, given that both contracts agree on the transfer and the requested transfer fee is paid.
However, this feature is to be used with caution, because there is a risk of hijacking management rights, requesting a high fee for getting (back) management rights of shares.
This is why the recommended way (that is implemented in QX) is that the owner/possessor needs to invoke a user procedure that actively releases the management rights by calling `qpi.releaseShares()`.
QX never releases shares passively (following call of `qpi.acquireShares()` by another contract).
The callbacks `PRE_RELEASE_SHARES()` and `PRE_ACQUIRE_SHARES()` may also check that the `qpi.originator()` initiating the transfer is the owner/possessor.
