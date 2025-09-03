---
sidebar_position: 2
---

# Testing

## Smart Contract Test Structure

Let's break down the test we wrote to verify the `MYTEST` contract:

```cpp
#define NO_UEFI

#include "contract_testing.h"

class ContractTestingMyTest : protected ContractTesting {
public:
    ContractTestingMyTest()
    {
        initEmptySpectrum();
        initEmptyUniverse();
        INIT_CONTRACT(MYTEST);
    }

    MYTEST::Add_output Add(sint64 a, sint64 b) {
        MYTEST::Add_input input;
        MYTEST::Add_output output;
        input.a = a;
        input.b = b;
        callFunction(MYTEST_CONTRACT_INDEX, 1, input, output);
        return output;
    }
};

TEST(MyTest, TestAdd) {
    ContractTestingMyTest test;
    MYTEST::Add_output output = test.Add(1, 2);
    EXPECT_EQ(output.c, 3);
}
```

We define `#define NO_UEFI` because the test is executed in a standard OS environment, not within UEFI:

```cpp
#define NO_UEFI
```

Include the testing framework:

```cpp
#include "contract_testing.h"
```

The `ContractTesting` base class provides the interface and logic needed to test Qubic contracts. Contract interactions such as function calls or procedure invocations must happen within a subclass like `ContractTestingMyTest`:

```cpp
class ContractTestingMyTest : protected ContractTesting {}
```

The constructor initializes the test environment:

- `initEmptySpectrum()` initializes the storage for user QUs.
- `initEmptyUniverse()` sets up the asset universe.
- `INIT_CONTRACT(MYTEST);` loads our contract into the testing runtime.

```cpp
    ContractTestingMyTest()
    {
        initEmptySpectrum();
        initEmptyUniverse();
        INIT_CONTRACT(MYTEST);
    }
```

:::info
You can skip `initEmptySpectrum()` or `initEmptyUniverse()` if your test doesn't involve QUs or assets.
:::

:::warning
If `MyTest` contract calls functions or procedures from `XXX` contract, you must also need `INIT_CONTRACT(XXX);`
:::

To test the `Add` function, we call `callFunction` with:

- The contract index (`MYTEST_CONTRACT_INDEX`)
- The registered function ID (`1`)
- The `input` and `output` structs

After the call, `output` contains the result returned by the contract:

```cpp
MYTEST::Add_output Add(sint64 a, sint64 b) {
  MYTEST::Add_input input;
  MYTEST::Add_output output;
  input.a = a;
  input.b = b;
  callFunction(MYTEST_CONTRACT_INDEX, 1, input, output);
  return output;
}
```

Finally, we define the test case using the `TEST` macro. We create a `ContractTestingMyTest` instance, call the `Add` function with values `1` and `2`, and assert the result is `3`:

```cpp
TEST(MyTest, TestAdd) {
    ContractTestingMyTest test;
    MYTEST::Add_output output = test.Add(1, 2);
    EXPECT_EQ(output.c, 3);
}
```

:::info
Calling `INIT_CONTRACT()` will reset the contract state. So each time you create an instance of `ContractTestingMyTest` will reset the contract state, spectrum and the universe.
:::

## Invoke User Procedure

We have learned how to call contract function above, pretty simple right? Now let's learn how we can call our procedure from our test

Assumming we have the below procedure in our contract :

```cpp
sint64 myNumber;

struct setMyNumber_input {
  sint64 myNumber;
};

struct setMyNumber_output {
};

PUBLIC_PROCEDURE(setMyNumber) {
  state.myNumber = input.myNumber;
}

REGISTER_USER_FUNCTIONS_AND_PROCEDURES() {
  REGISTER_USER_PROCEDURE(setMyNumber, 1);
}
```

So the test code will looke like:

```cpp
class ContractTestingMyTest : protected ContractTesting {
public:
...

MYTEST::setMyNumber_output setMyNumber(id user, sint64 number) {
  MYTEST::setMyNumber_input input;
  MYTEST::setMyNumber_output output;
  input.myNumber = number;
  EXPECT_TRUE(invokeUserProcedure(MYTEST_CONTRACT_INDEX, 1, input, output, user, 0));
  return output;
}

...
}

TEST(MyTest, SetMyNumber) {
  ContractTestingMyTest test;
  // Although the contract doesn't require QUs for execution,
  // the caller must exist in the spectrum (i.e., have at least 1 QU)
  // in order to successfully invoke a procedure.
  increaseEnergy(user, 1'000'000); // Give user 1M QUs
  MYTEST::setMyNumber_output output = test.setMyNumber(user, 42);
}

```

It’s almost like calling a function, right? But there are some differences.

To invoke a procedure, we use the `invokeUserProcedure` function. The first argument is the contract index, the second is the procedure ID, followed by the input and output structs.

Since invoking a procedure in Qubic is actually make a transaction, we must also provide the sender (the user who creates the transaction) and the amount of QUs being transferred — which is 0 in our case.

Finally, we check the return value of `invokeUserProcedure` to ensure the procedure call was successful by asserting it returns `true`.

:::warning
Calling `increaseEnergy()` without `initEmptySpectrum()` without throw error at runtime.  
:::

## Query Contract State

We have successfully invoked our procedure to set the `myNumber` state. But how can we verify that it was actually updated?

There are two ways to query the contract state in our test. Let's explore them now.

### 1. Use Function To Query State

This is the traditional way to query state in both our tests and the real production environment. We simply create a function in our contract that returns the `myNumber` state, then call this function from our test.

Let's see how to write this:

```cpp

struct getMyNumber_input {
};

struct getMyNumber_output {
  sint64 myNumber;
};

PUBLIC_FUNCTION(getMyNumber) {
  output.myNumber = state.myNumber;
}


REGISTER_USER_FUNCTIONS_AND_PROCEDURES() {
  REGISTER_USER_FUNCTION(getMyNumber, 1);
}

```

And then call the `getMyNumber` in our test:

```cpp
class ContractTestingMyTest : protected ContractTesting {
public:
// ...

MYTEST::setMyNumber_output setMyNumber(id user, sint64 number) {
  // ...
}

MYTEST::getMyNumber_output getMyNumber() {
  MYTEST::getMyNumber_input input;
  MYTEST::getMyNumber_output output;
  callFunction(MYTEST_CONTRACT_INDEX, 1, input, output);
  return output;
}

// ...
}

TEST(MyTest, SetAndGetMyNumber) {
  ContractTestingMyTest test;
  // Although the contract doesn't require QUs for execution,
  // the caller must exist in the spectrum (i.e., have at least 1 QU)
  // in order to successfully invoke a procedure.
  increaseEnergy(user, 1'000'000); // Give user 1M QUs
  MYTEST::setMyNumber_output output = test.setMyNumber(user, 42);

  MYTEST::getMyNumber_output getOutput = test.getMyNumber();
  // The myNumber state should be 42
  EXPECT_EQ(getOutput.myNumber, 42);
}
```

### 2. Use Contract Instance To Query State

As shown, the state is members of the contract struct. This means that once we have an instance of the contract, we can directly access its state.

A pointer to the contract instance is stored in the `contractStates` array. To retrieve our contract's pointer, we simply access it using the contract index `contractStates[NAME_CONTRACT_INDEX]`:

```cpp
TEST(MyTest, SetMyNumber) {
  ContractTestingMyTest test;
  increaseEnergy(user, 1'000'000);
  MYTEST::setMyNumber_output output = test.setMyNumber(user, 42);

  char* state = (char*)contractStates[MYTEST_CONTRACT_INDEX];
  // Read the first 64 bits from state pointer and cast it to sint64 type
  EXPECT_EQ(*((sint64*)state), 42);
}
```

Now you can query the state without creating a contract function. However, this approach still feels a bit messy since it involves handling pointers.

A cleaner solution is to create a struct that inherits from the state struct and implement a function to retrieve `myNumber`:

```cpp
struct MYTESTGetter : public MYTEST {
    sint64 getMyNumber() {
        return this->myNumber;
    }
};

TEST(MyTest, SetMyNumber) {
  ContractTestingMyTest test;
  increaseEnergy(user, 1'000'000);
  MYTEST::setMyNumber_output output = test.setMyNumber(user, 42);

  // Cast the pointer to MYTESTGetter pointer so we can call our getMyNumber()
  MYTESTGetter* state = (MYTESTGetter*)contractStates[MYTEST_CONTRACT_INDEX];
  EXPECT_EQ(state->getMyNumber(), 42);
}
```

## Invoke System Procedure

In the test environment, we can directly invoke system procedures to verify whether our logic works correctly.

:::note
But keep in mind: when we deploy our contract, system procedures are automatically triggered by the Qubic network and **cannot be invoked manually.**
:::

```cpp
class ContractTestingMyTest : protected ContractTesting {
public:
// ...

void beginEpoch() {
  callSystemProcedure(MYTEST_CONTRACT_INDEX, BEGIN_EPOCH);
}

void endEpoch() {
  callSystemProcedure(MYTEST_CONTRACT_INDEX, END_EPOCH);
}

// ...
}

TEST(MyTest, TestBeginEpoch) {
  ContractTestingMyTest test;

  test.beginEpoch();
  test.endEpoch();
}
```

## Mock Data

As mentioned in [QPI date and time functions](<(/smart-contract/qpi#qpiyearmonthdayhourminutesecondmillisecondtickepochdayofweek)>), they will not work correctly in the test environment without mocking the data (for example, `qpi.epoch()` will always return `0`).

So, how can we mock this data?

### qpi.epoch()

```cpp
TEST(MyTest, TestEpoch) {
  system.epoch = 199;

  // In contract call qpi.epoch() will return 199
  // output.epoch = qpi.epoch()
}
```

### qpi.tick()

```cpp
TEST(MyTest, TestEpoch) {
  system.tick = 2000;

  // In contract call qpi.tick() will return 2000
  // output.tick = qpi.tick()
}
```

### qpi.year|month|day|hour|minute|second|millisecond()

```cpp
TEST(MyTest, TestEpoch) {
  // To set current date for the core environment
  updateTime();
  // Then reflect it to qpi
  updateQpiTime();
  // Now qpi.year() or qpi.month(), ... will return correct value

  // We can also set time to any number
  utcTime.Year = 2025;
  utcTime.Month = 10;
  utcTime.Day = 15;
  // ...
  // Then reflect it to qpi
  updateQpiTime();
}
```
