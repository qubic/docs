---
sidebar_position: 2
---

# Add Your Contract

Now let’s add your custom contract to the Qubic project.
It’s not too difficult, though it can feel a bit tangled at first—but don’t worry, we’ll guide you through it step by step and make it feel simple!

## Naming contract rules

Pick a **unique name** for your contract. You’ll need:

- **Long name**: For the filename (e.g. `YourContractName.h`)
- **Short name**: Max 7 capital letters/digits (e.g. `YCN`, used as asset name)
- **Optional full-uppercase name**: For state struct and global constants (e.g. `YOURCONTRACTNAME`)

**Examples:**

- `Quottery.h`, asset: `QTRY`, state struct: `QUOTTERY`
- `Qx.h`, asset: `QX`, state struct: `QX`

## Let's add the contract

:::warning To fix Visual Studio don't write change to disk
Do **Project → Show All Files** first before adding the contract
:::

Let's say we want to name our contract is **MyTest** then we will create a file `MyTest.h` at `Qubic` project at location `/contracts/MyTest.h` with the content

```cpp title="MyTest.h"
using namespace QPI;

struct MYTEST2
{
};

struct MYTEST : public ContractBase
{
public:
    struct add_input
    {
        sint64 a;
        sint64 b;
    };

    struct add_output
    {
        sint64 out;
    };

    PUBLIC_FUNCTION(add)
    {
        output.out = input.a + input.b;
    }

    REGISTER_USER_FUNCTIONS_AND_PROCEDURES()
    {
        REGISTER_USER_FUNCTION(add, 1);
    }
};
```

## Define the contract

After creating the contract, we need to define it—just like how a newborn baby needs a name.

**1. Define the CONTRACT_INDEX and STATE**

- At `Qubic` project go to `/contract_core` folder
- Open the file `contract_def.h`
- Search for the first "// new contracts should be added above this line"

You will see something like this

```cpp title="/contract_core/contract_def.h"
// ...
#undef CONTRACT_INDEX
#undef CONTRACT_STATE_TYPE
#undef CONTRACT_STATE2_TYPE

#define MSVAULT_CONTRACT_INDEX 11
#define CONTRACT_INDEX MSVAULT_CONTRACT_INDEX
#define CONTRACT_STATE_TYPE MSVAULT
#define CONTRACT_STATE2_TYPE MSVAULT2
#include "contracts/MsVault.h"

#undef CONTRACT_INDEX
#undef CONTRACT_STATE_TYPE
#undef CONTRACT_STATE2_TYPE

#define QBAY_CONTRACT_INDEX 12
#define CONTRACT_INDEX QBAY_CONTRACT_INDEX
#define CONTRACT_STATE_TYPE QBAY
#define CONTRACT_STATE2_TYPE QBAY2
#include "contracts/Qbay.h"

// new contracts should be added above this line
// ...
```

- Now add your contract defination before the comment line

```cpp title="/contract_core/contract_def.h"
// ...
#undef CONTRACT_INDEX
#undef CONTRACT_STATE_TYPE
#undef CONTRACT_STATE2_TYPE

#define MSVAULT_CONTRACT_INDEX 11
#define CONTRACT_INDEX MSVAULT_CONTRACT_INDEX
#define CONTRACT_STATE_TYPE MSVAULT
#define CONTRACT_STATE2_TYPE MSVAULT2
#include "contracts/MsVault.h"

#undef CONTRACT_INDEX
#undef CONTRACT_STATE_TYPE
#undef CONTRACT_STATE2_TYPE

#define QBAY_CONTRACT_INDEX 12
#define CONTRACT_INDEX QBAY_CONTRACT_INDEX
#define CONTRACT_STATE_TYPE QBAY
#define CONTRACT_STATE2_TYPE QBAY2
#include "contracts/Qbay.h"

/* ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ */

#undef CONTRACT_INDEX
#undef CONTRACT_STATE_TYPE
#undef CONTRACT_STATE2_TYPE

#define MYTEST_CONTRACT_INDEX 13 // previous contract number + 1
#define CONTRACT_INDEX MYTEST_CONTRACT_INDEX
#define CONTRACT_STATE_TYPE MYTEST
#define CONTRACT_STATE2_TYPE MYTEST2
#include "contracts/MyTest.h"

/* ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ */

// new contracts should be added above this line
// ...
```

**2. Define the contract discription**

- Search for the next "// new contracts should be added above this line"

You will see something like this

```cpp title="/contract_core/contract_def.h"
// ...
constexpr struct ContractDescription
{
    char assetName[8];
    // constructionEpoch needs to be set to after IPO (IPO is before construction)
    unsigned short constructionEpoch, destructionEpoch;
    unsigned long long stateSize;
} contractDescriptions[] = {
    {"", 0, 0, sizeof(Contract0State)},
    {"QX", 66, 10000, sizeof(QX)},
    {"QTRY", 72, 10000, sizeof(QUOTTERY)},
    {"RANDOM", 88, 10000, sizeof(IPO)},
    {"QUTIL", 99, 10000, sizeof(QUTIL)},
    {"MLM", 112, 10000, sizeof(IPO)},
    {"GQMPROP", 123, 10000, sizeof(GQMPROP)},
    {"SWATCH", 123, 10000, sizeof(IPO)},
    {"CCF", 127, 10000, sizeof(CCF)}, // proposal in epoch 125, IPO in 126, construction and first use in 127
    {"QEARN", 137, 10000, sizeof(QEARN)}, // proposal in epoch 135, IPO in 136, construction in 137 / first donation after END_EPOCH, first round in epoch 138
    {"QVAULT", 138, 10000, sizeof(IPO)}, // proposal in epoch 136, IPO in 137, construction and first use in 138
    {"MSVAULT", 149, 10000, sizeof(MSVAULT)}, // proposal in epoch 147, IPO in 148, construction and first use in 149
    {"QBAY", 154, 10000, sizeof(QBAY)}, // proposal in epoch 152, IPO in 153, construction and first use in 154
    // new contracts should be added above this line
// ...
```

- Now let's add our contract description `{"MYTEST", 999, 10000, sizeof(MYTEST)}`

:::note
The format is `{"CONTRACT_ASSET_NAME", CONSTRUCTION_EPOCH, DESTRUCTION_EPOCH, SIZE_OF_STATE}` and `CONSTRUCTION_EPOCH & DESTRUCTION_EPOCH` can be any number in test environment.
:::

```cpp title="/contract_core/contract_def.h"
// ...
constexpr struct ContractDescription
{
    char assetName[8];
    // constructionEpoch needs to be set to after IPO (IPO is before construction)
    unsigned short constructionEpoch, destructionEpoch;
    unsigned long long stateSize;
} contractDescriptions[] = {
    {"", 0, 0, sizeof(Contract0State)},
    {"QX", 66, 10000, sizeof(QX)},
    {"QTRY", 72, 10000, sizeof(QUOTTERY)},
    {"RANDOM", 88, 10000, sizeof(IPO)},
    {"QUTIL", 99, 10000, sizeof(QUTIL)},
    {"MLM", 112, 10000, sizeof(IPO)},
    {"GQMPROP", 123, 10000, sizeof(GQMPROP)},
    {"SWATCH", 123, 10000, sizeof(IPO)},
    {"CCF", 127, 10000, sizeof(CCF)}, // proposal in epoch 125, IPO in 126, construction and first use in 127
    {"QEARN", 137, 10000, sizeof(QEARN)}, // proposal in epoch 135, IPO in 136, construction in 137 / first donation after END_EPOCH, first round in epoch 138
    {"QVAULT", 138, 10000, sizeof(IPO)}, // proposal in epoch 136, IPO in 137, construction and first use in 138
    {"MSVAULT", 149, 10000, sizeof(MSVAULT)}, // proposal in epoch 147, IPO in 148, construction and first use in 149
    {"QBAY", 154, 10000, sizeof(QBAY)}, // proposal in epoch 152, IPO in 153, construction and first use in 154
    /* ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ */
    {"MYTEST", 999, 10000, sizeof(MYTEST)}, // {"ASSET_NAME", CONSTRUCTION_EPOCH, DESTRUCTION_EPOCH, SIZE_OF_STATE}
    // new contracts should be added above this line

// ...
```

**3. Register contract**

- Search for the 3rd "// new contracts should be added above this line"

You will see something like this

```cpp title="/contract_core/contract_def.h"
// ...
static void initializeContracts()
{
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QX);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QUOTTERY);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(RANDOM);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QUTIL);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(MLM);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(GQMPROP);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(SWATCH);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(CCF);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QEARN);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QVAULT);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(MSVAULT);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QBAY);
    // new contracts should be added above this line
#ifdef INCLUDE_CONTRACT_TEST_EXAMPLES
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXA);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXB);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXC);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXD);
#endif
}
// ...
```

- Add `REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(MYTEST);` before the comment line

```cpp title="/contract_core/contract_def.h"
// ...
static void initializeContracts()
{
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QX);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QUOTTERY);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(RANDOM);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QUTIL);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(MLM);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(GQMPROP);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(SWATCH);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(CCF);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QEARN);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QVAULT);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(MSVAULT);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(QBAY);
    /* ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ */
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(MYTEST);
    // new contracts should be added above this line
#ifdef INCLUDE_CONTRACT_TEST_EXAMPLES
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXA);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXB);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXC);
    REGISTER_CONTRACT_FUNCTIONS_AND_PROCEDURES(TESTEXD);
#endif
}
// ...
```

👉 Now that we have our contract ready, how do we test it? Let's find out in the next section.
