---
title: Types Of Call And Invoke
sidebar_position: 7
---

#

## Inner-Contract Call

Inner-contract calls occur when a Qubic smart contract invokes its own functions or procedures to modularize logic, reuse code, and manage state efficiently. Unlike cross-contract calls, these execute entirely within the same contract’s scope.

**Macro**

```cpp
#define CALL(functionOrProcedure, input, output)
```

**Example Code**

Below program is to calculate sum 1 to 10 and square the sum:

```cpp
///////////// Square Function /////////////
struct square_input
{
    sint64 a;
};

struct square_output
{
    sint64 out;
};

// We should private the function that only used internally
PRIVATE_FUNCTION(square)
{
    output.out = input.a * input.a;
}

///////////// SumSquareOneToTen Function /////////////

struct sumSquareOneToTen_input
{
};

struct sumSquareOneToTen_output
{
    sint64 sum;
};

struct sumSquareOneToTen_locals
{
    sint64 i;
    // Define input and output for the call also need to be in locals
    square_input squareInput;
    square_output squareOutput;
};

PUBLIC_FUNCTION_WITH_LOCALS(sumSquareOneToTen)
{
    for (locals.i = 1; locals.i <= 10; ++locals.i)
    {
        output.sum += locals.i;
    }
    locals.squareInput.a = output.sum;
    CALL(square, locals.squareInput, locals.squareOutput);
    output.sum = locals.squareOutput.out;
}
```

## Cross-Contract Call

Cross-contract calls enable Qubic smart contracts to interact with each other, allowing for modular and reusable blockchain logic. Unlike inner-contract calls, which execute within the same contract, cross-contract calls invoke functions or procedures in external contracts, facilitating complex decentralized applications (dApps) and interoperable protocols.

**Macros**

```cpp
#define CALL_OTHER_CONTRACT_FUNCTION(contractStateType, function, input, output)
#define INVOKE_OTHER_CONTRACT_PROCEDURE(contractStateType, procedure, input, output, invocationReward)
```

:::warning INVOKE_OTHER_CONTRACT_PROCEDURE
Your contract will pay `invocationReward` amount of Qubic if the invoked contract consume these.
:::

**Example Code**

Let’s create an additional contract to interact with it.

:::warning
Make sure to define the `Cross` contract in `contract_def.h` with a lower index and position it before the `MyTest` definition.
:::

```cpp title="Cross.h"
#pragma once

using namespace QPI;

struct CROSS2
{
};

struct CROSS : public ContractBase
{
    public:
        sint64 crossStateNumber;

        struct setCrossStateNumber_input
        {
            sint64 crossStateNumber;
        };

        struct setCrossStateNumber_output
        {
        };

        PUBLIC_PROCEDURE(setCrossStateNumber)
        {
            state.crossStateNumber = input.crossStateNumber;
        }

        struct getCrossStateNumber_input
        {
        };

        struct getCrossStateNumber_output
        {
            sint64 crossStateNumber;
        };

        PUBLIC_FUNCTION(getCrossStateNumber)
        {
            output.crossStateNumber = state.crossStateNumber;
        }

        REGISTER_USER_FUNCTIONS_AND_PROCEDURES()
        {
          REGISTER_USER_PROCEDURE(setCrossStateNumber, 1);
          REGISTER_USER_FUNCTION(getCrossStateNumber, 1);
        }
};
```

Let's now try to invoke the `setCrossStateNumber` of `Cross` from `MyTest` contract

```cpp title="MyTest.h"
using namespace QPI;

struct MYTEST2
{
};

struct MYTEST : public ContractBase
{
  public:

        struct crossSetStateNumberInMyTest_input
        {
            sint64 crossStateNumber;
        };

        struct crossSetStateNumberInMyTest_output
        {
            bit success;
        };

        struct crossSetStateNumberInMyTest_locals
        {
            // Input and Output the CROSS procedure invoke
            CROSS::setCrossStateNumber_input crossInputProcedure;
            CROSS::setCrossStateNumber_output crossOutputProcedure;
            // Input and Output the CROSS function invoke
            CROSS::getCrossStateNumber_input crossGetInputFunction;
            CROSS::getCrossStateNumber_output crossGetOutputFunction;

            sint64 crossStateNumber;
        };

        PUBLIC_PROCEDURE_WITH_LOCALS(crossSetStateNumberInMyTest)
        {
            locals.crossInputProcedure.crossStateNumber = input.crossStateNumber;
            // Set the cross state number in the CROSS contract
            INVOKE_OTHER_CONTRACT_PROCEDURE(CROSS, setCrossStateNumber, locals.crossInputProcedure, locals.crossOutputProcedure, qpi.invocationReward());
            // Now get the cross state number from the CROSS contract
            CALL_OTHER_CONTRACT_FUNCTION(CROSS, getCrossStateNumber, locals.crossGetInputFunction, locals.crossGetOutputFunction);

            locals.crossStateNumber = locals.crossGetOutputFunction.crossStateNumber;
            // Check if the cross state number is set correctly
            if (locals.crossStateNumber != input.crossStateNumber)
            {
              output.success = false;
            }
            else
            {
              output.success = true;
            }
        }

        REGISTER_USER_FUNCTIONS_AND_PROCEDURES()
        {
            REGISTER_USER_PROCEDURE(crossSetStateNumberInMyTest, 10);
        }
};

```

:::warning
If your contract calls a function or procedure from another contract, you must also call `INIT_CONTRACT()` for that contract in test environment.
:::

## Rules & Best Practices

### Allowed Patterns

✅ Function → Function

✅ Procedure → Procedure

✅ Procedure → Function

### Restricted Patterns

❌ Function → Procedure (Functions cannot modify state)

### Best Practices

- **Use `PRIVATE` Scope**
  - Restrict inner calls to `PRIVATE_FUNCTION/PRIVATE_PROCEDURE` unless external access is needed.
