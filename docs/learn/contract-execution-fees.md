# Contract Execution Fees

## Overview

Every smart contract in Qubic has an **execution fee reserve** that determines whether the contract can execute its procedures. This reserve is initially funded during the contract's IPO (Initial Public Offering). Contracts must maintain a positive execution fee reserve to remain operational. It is important to note that these execution fees are different from the fees a user pays to a contract upon calling a procedure. To avoid confusion we will call the fees a user pays to a contract 'invocation reward' throughout this document.

## Fee Management

The current value of the executionFeeReserve can be queried via the Qubic Programming Interface (QPI) or via the QUtil smart contract.

When a contract's IPO completes, the execution fee reserve is initialized based on the IPO's final price. If all shares were sold during the IPO, the reserve is set to `finalPrice * NUMBER_OF_COMPUTORS` (676 computors). However, if the IPO fails, i.e. not all shares are sold, the contract is marked with an error and the reserve remains 0 and cannot be filled anymore. A contract which failed the IPO will remain unusable.

Contracts can refill their execution fee reserves in the following ways:

- **Contract internal burning**: Any contract procedure can burn its own QU to refill its own reserve or to refill another contract's reserve.
- **External refill via QUtil**: Anyone can refill any contract's reserve by sending QU to the QUtil contract's `BurnQubicForContract` procedure with the target contract index. All sent QU is burned and added to the target contract's reserve.
- **Legacy QUtil burn**: QUtil provides a `BurnQubic` procedure that burns to QUtil's own reserve specifically.

The execution fee system follows a key principle: **"The Contract Initiating Execution Pays"**. When a user initiates a transaction, the user's destination contract must have a positive executionFeeReserve. When a contract initiates an operation (including any callbacks it triggers), that contract must have positive executionFeeReserve.

The execution time of each contract is measured and fees proportional to that execution time are deducted from the reserve.
If the fee reserve of a contract goes to or below 0, the contract becomes dormant.
This means, it will mostly be unusable until the reserve is refilled (for exceptions see next section).

## What Operations Require Execution Fees

The execution fee system checks whether a contract has positive execution fee reserve at different entry points.
Contract user functions are never checked and their execution time does not contribute to the overall fee.
Contract procedures generally only run with positive reserve and their execution time contributes to the fee.
There are some special system procedures and callbacks that will run even with non-positive reserve to ensure overall operation of the Qubic network, however, their execution time still contributes to the deducted fee.
For details, please see [this developer documentation](https://github.com/qubic/core/blob/main/doc/execution_fees.md#what-operations-require-execution-fees).

## Consolidating Fees Across Computors

To ensure that the state of the Qubic network stays consistent across all nodes, each computor has to deduct the same execution fee amount for each contract.
However, the actual execution time will vary due e.g. different hardware setups.
To account for that, each computor can define their own multiplier to scale the raw execution time. 
To consolidate the scaled execution times from each computor into a single consistent execution fee value, the quorum value is used.

Every computor sends their scaled execution time to the network as transaction.
After all transactions are sent, the received execution fee values are sorted in ascending order and the value at the quorum position `2/3 * NUMBER_OF_COMPUTORS + 1 = 451` is taken as final execution fee to be deducted. 

## Best Practices

### For Contract Developers

1. **Plan for sustainability**: Charge invocation rewards for running user procedures.
2. **Burn collected invocation rewards**: Regularly burn QUs to replenish the execution fee reserve.
3. **Monitor reserve**: Implement a function to expose current reserve level.
4. **Graceful degradation**: Consider what happens when reserve runs low.
5. **Handle inter-contract call errors**: After calling procesdures of another contract, verify that the call succeeded. Handle errors gracefully (e.g., skip operations, use fallback logic). You can also proactively verify the called contract has positive fee reserve using the query function provided in QPI before calling.

### For Contract Users

1. **Check contract status**: Before using a contract, verify it has positive execution fee reserve.
2. **Transaction failures**: If your transaction fails due to insufficient execution fees reserve, the attached amount will be automatically refunded.
3. **No funds lost**: The system ensures amounts are refunded if a contract cannot execute.

