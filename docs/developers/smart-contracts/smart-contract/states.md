---
sidebar_position: 6
---

# States

The state refers to the persistent data of a contract — essentially the member variables defined within the contract struct. It holds the current values of the contract and must remain **identical across all nodes** in the Qubic network to maintain deterministic execution and consensus. Any modification to the state must be performed carefully through defined procedures.

The contract state is passed to the functions & procedures as a reference named `state`.

**1. Example how to create a state number**

The `myNumber` variable is called state of the `MYTEST` contract

```cpp
struct MYTEST : public ContractBase
{
public:
  sint64 myNumber;
};
```

**1. Example how to modify state number**

```cpp
struct MYTEST : public ContractBase
{
public:
  sint64 myNumber;

  struct changeNumber_input
  {
    sint64 myNumber;
  };

  struct changeNumber_output
  {
  };

  // Reminder: The contract state is passed to the functions & procedures
  // as a reference named `state`.
  PUBLIC_PROCEDURE(changeNumber)
  {
    // myNumber = input.myNumber; is wrong
    state.myNumber = input.myNumber;
  }

  // WRONG, function can't modify state
  // PUBLIC_FUNCTION(changeNumber)
  // {
  //   state.myNumber = input.myNumber;
  // }
};
```

:::warning
Attempting to modify the state inside a function will result in the error "expression must be a modifiable lvalue", because functions are not allowed to change contract state.
:::

:::info
The memory available to the contract is allocated statically, but extending the state will be possible between epochs through special `EXPAND` events (this event is not implemented yet).
:::
