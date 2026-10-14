---
sidebar_position: 6
---

# States

The state refers to the persistent data of a contract — all member variables declared inside the nested `struct StateData` of the contract struct. It holds the current values of the contract and must remain **identical across all nodes** in the Qubic network to maintain deterministic execution and consensus. Any modification to the state must be performed carefully through defined procedures.

The contract state is passed to the functions & procedures as a `ContractState` wrapper named `state`:

- `state.get()` returns a **read-only** reference to `StateData`. Available in functions and procedures.
- `state.mut()` returns a **writable** reference to `StateData` and marks the state as changed. Available in procedures only.

:::note
Only contracts whose state was accessed via `state.mut()` during a tick get their state digest recomputed at the end of that tick. Use `state.get()` whenever you only read.
:::

**1. Example how to create a state number**

The `myNumber` variable is called state of the `MYTEST` contract

```cpp
struct MYTEST : public ContractBase
{
    struct StateData
    {
        sint64 myNumber;
    };
};
```

**2. Example how to read and modify state number**

```cpp
struct MYTEST : public ContractBase
{
    struct StateData
    {
        sint64 myNumber;
    };

    struct changeNumber_input
    {
        sint64 myNumber;
    };

    struct changeNumber_output
    {
    };

    struct getNumber_input
    {
    };

    struct getNumber_output
    {
        sint64 myNumber;
    };

    // Reminder: The contract state is passed to the functions & procedures
    // as a `ContractState` wrapper named `state`.
    PUBLIC_PROCEDURE(changeNumber)
    {
        // myNumber = input.myNumber; and state.myNumber = input.myNumber; are wrong
        state.mut().myNumber = input.myNumber;
    }

    PUBLIC_FUNCTION(getNumber)
    {
        output.myNumber = state.get().myNumber;
    }

    // WRONG, function can't modify state (no state.mut() in functions)
    // PUBLIC_FUNCTION(changeNumber)
    // {
    //     state.mut().myNumber = input.myNumber;
    // }
};
```

:::warning
Inside a function `state` is const, so calling `state.mut()` does not compile (e.g. clang: `'this' argument to member function 'mut' has type 'const QPI::ContractState<...>', but function is not marked const`). Writing through `state.get()` fails as well, because it returns a const reference.
:::

**3. Containers and structs in the state**

Members of `StateData` are accessed the same way, also when they are structs or QPI containers:

```cpp
struct StateData
{
    HashMap<id, sint64, 1024> balances;
    Array<id, 256> players;
    uint64 playerCount;
};

// read
state.get().balances.get(qpi.invocator(), locals.balance);
locals.player = state.get().players.get(locals.i);

// write
state.mut().balances.set(qpi.invocator(), locals.balance + qpi.invocationReward());
state.mut().players.set(state.get().playerCount, qpi.invocator());
state.mut().playerCount++;
```

Helpers outside the QPI macros take the wrapper type:

```cpp
static void resetRound(QPI::ContractState<StateData, CONTRACT_INDEX>& state)
{
    state.mut().playerCount = 0;
}
```

:::info
The memory available to the contract is allocated statically, but extending the state will be possible between epochs through special `EXPAND` events (this event is not implemented yet).
:::

## Changing the state layout

When an update changes `StateData`, the old state file has to be converted. The change is requested in `contract_def.h` of the core:

```cpp
constexpr ContractStateChangeInfo contractStateChangeInfos[] = { { <contract_index>, <change_type>, <epoch> } };
```

- `PADDING`: zero-pads the old state file to the new size. Only works if new members are appended at the end of `StateData`.
- `RESET`: resets the whole state to 0. All previous data is lost.
- `MIGRATE`: loads the old state file and runs the contract's `MIGRATE` procedure to fill the new state.

The state change is only triggered if the size of `StateData` differs from the old state file.

For `MIGRATE`, the contract needs:

- A nested `struct OldStateData` with exactly the layout of the previous `StateData`.
- A `MIGRATE()` or `MIGRATE_WITH_LOCALS()` procedure. It gets `state` (new state), `oldState` (const `OldStateData&`) and optional `locals`.

```cpp
struct MYTEST : public ContractBase
{
    struct StateData
    {
        sint64 myNumber;
        uint64 changeCount; // new member
    };

    struct OldStateData
    {
        sint64 myNumber;
    };

    MIGRATE()
    {
        state.mut().myNumber = oldState.myNumber;
    }
};
```

:::warning
`MIGRATE` runs with a function context (`QpiContextFunctionCall`), so QPI calls that change the spectrum or universe (e.g. `qpi.transfer()`, `qpi.burn()`) are not available there.
:::
