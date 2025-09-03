---
sidebar_position: 5
---

# Procedures and Functions

In Qubic, contract logic is divided into functions and procedures, each serving a distinct purpose:

## Functions

User functions **cannot** modify the contract's state, but they are useful to query information from the state, either with the network message `RequestContractFunction`, or by a function or procedure of the same or another contract.

- **Example:**

```cpp
// PUBLIC_FUNCTION can be called by other contracts
PUBLIC_FUNCTION(MyFunc) {
  // code
}
```

```cpp
// PRIVATE_FUNCTION are only available in current contract
PRIVATE_FUNCTION(MyFunc) {
  // code
}
```

:::note
Functions can be called by procedures, but procedures cannot be called by functions.
:::

## Procedures

User procedures **can** modify the state. They are invoked either by transactions with the ID (public key) of the contract being the destination address, or from another procedure of the same contract or a different contract.

- **Example**

```cpp
// A PUBLIC procedure can be called by other contracts with larger
// contract index (contracts deployed after).
PUBLIC_PROCEDURE(UpdateBalance) {
  state.balance += input.amount;
}
```

```cpp
// A PRIVATE procedure cannot be called by other contracts.
PRIVATE_PROCEDURE(UpdateBalance) {
  state.balance += input.amount;
}
```

## Input & Ouput

Too receive input and return output in functions & procedures we need to define the struct `[NAME]_input` and `[NAME]_output`. A reference to an instance of `[NAME]_input` named `input` is passed to functions & procedures containing the input data. Further, a reference to an instance of `[NAME]_output` named `output` is passed to the functions & procedures (initialized with zeros), which should be modified.

**1. Example how to declare input and output for Square function**

```cpp
struct Square_input {
  sint64 x;
};

struct Square_output {
  sint64 result;
};

PUBLIC_FUNCTION(Square) {
  output.result = input.x * input.x;
}
```

**2. Example how to declare input and output for SetPrice procedure**

```cpp
struct SetPrice_input {
  sint64 price;
};

// Leave output empty if not used
struct SetPrice_output {
};

PUBLIC_PROCEDURE(SetPrice) {
  state.price = input.price;
}
```

:::note
Procedures's ouput is returned if the procedure is invoked from another procedure, but unused if the procedure has been invoked directly through a transaction.
:::

## System Procedure

System procedures can modify the state and are invoked by the Qubic Core (the system) as event callbacks.

They are defined with the following macros:

| Procedure                        | Description                                                                                                                                                                                   |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. INITIALIZE()**              | Called once after a successful IPO, just before the construction epoch begins, to initialize the contract state.                                                                              |
| **2. BEGIN_EPOCH()**             | Called at the start of each epoch, after node startup or seamless epoch transition, and before the first tick (`BEGIN_TICK()`).                                                               |
| **3. END_EPOCH()**               | Called after each epoch ends, after the last `END_TICK()`, and before (1) contract shares are generated (IPO), (2) revenue and donations are distributed, and (3) the epoch counter advances. |
| **4. BEGIN_TICK()**              | Called before each tick is processed (i.e., before executing the tick’s transactions).                                                                                                        |
| **5. END_TICK()**                | Called after all transactions in a tick have been executed.                                                                                                                                   |
| **6. PRE_RELEASE_SHARES()**      | Called before this contract transfers asset management rights to another contract using `qpi.acquireShare()`.                                                                                 |
| **7. PRE_ACQUIRE_SHARES()**      | Called before this contract receives asset management rights from another contract using `qpi.releaseShare()`.                                                                                |
| **8. POST_RELEASE_SHARES()**     | Called after this contract has transferred asset management rights to another contract via `qpi.acquireShare()`.                                                                              |
| **9. POST_ACQUIRE_SHARES()**     | Called after this contract has received asset management rights from another contract via `qpi.releaseShare()`.                                                                               |
| **10. POST_INCOMING_TRANSFER()** | Called after QUs have been transferred to this contract.                                                                                                                                      |

**1. Example to use BEGIN_EPOCH procedure**

```cpp
// Increase number every epoch
BEGIN_EPOCH() {
  state.number++;
}
```

:::note
System procedures 1 to 5 have no input and output. The input and output of system procedures 6 to 9 are discussed in the section about [Assets And Shares](/smart-contract/assets-and-shares.md).
:::

## Local Variables

In QUBIC contract creating local variables / objects on the regular function call stack is **forbidden**. If we want to use local variable (eg. tmp variables, `i` for the `forloop`) we will need help of postfix `_WITH_LOCALS` before declare Function and Procedure macros. Function and Procedure end with `_WITH_LOCALS` have to define the struct `[NAME]_locals`. A reference to an instance of `[NAME]_locals` named `locals` is passed to the function and procedure (initialized with zeros).

**1. Example how to use locals variable**

```cpp
struct SumOneToTen_input {
  // no input fields
};

struct SumOneToTen_output {
  sint64 sum;
};

struct SumOneToTen_locals {
  sint64 i;
};

PUBLIC_FUNCTION_WITH_LOCALS(SumOneToTen) {
  // Reminder: A reference to an instance of `[NAME]_locals` named `locals`
  // is passed to the function and procedure (initialized with zeros).
  for (locals.i = 1; locals.i <= 10; ++locals.i) {
    output.sum += locals.i;
  }
}
```

## Register Function And Procedure

In order to make the function and procedure available you need to call `REGISTER_USER_FUNCTION([NAME], [INPUT_TYPE]);` for function and `REGISTER_USER_PROCEDURE([NAME], [INPUT_TYPE]);` for procedure. `INPUT_TYPE` is the unique id of the funtion or the procedure.

`REGISTER_USER_FUNCTION` and `REGISTER_USER_PROCEDURE` must be called in `REGISTER_USER_FUNCTIONS_AND_PROCEDURES` block.

**1. Example how to register functions and procedure**

```cpp
PUBLIC_FUNCTION(MyFunc) {
}

PUBLIC_PROCEDURE(UpdateBalance) {
}

REGISTER_USER_FUNCTIONS_AND_PROCEDURES() {
  REGISTER_USER_FUNCTION(MyFunc, 1);
  // REGISTER_USER_FUNCTION(MyFunc2, 1); is WRONG, 2 functions can't have same id

  REGISTER_USER_PROCEDURE(UpdateBalance, 2);
  // REGISTER_USER_PROCEDURE(UpdateBalance2, 1); is OK
}
```

:::info
Two functions or two procedures cannot share the same id. However, a function and a procedure can use the same id without conflict.
:::
