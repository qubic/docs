---
sidebar_position: 4
---

# Contract Structure

Let's breakdown the adding contract we wrote before

```cpp
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

This line brings all QPI symbols into our current scope:

```cpp
using namespace QPI;
```

Every contract includes a `[CONTRACT]2` struct, which is used for state expansion via the `EXPAND` procedure. However, since that feature isn't implemented yet, you can ignore it for now:

```cpp
struct MYTEST2
{
};
```

This is the main contract structure, where the state and logic reside. Inheriting from ContractBase is mandatory:

```cpp
struct MYTEST : public ContractBase
{
};
```

This is a simple example of how to write a contract function that takes two numbers and returns their sum. Further details will be explained in a later section.

```cpp
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

```

To make this function callable, we need to register it and assign it a unique numeric ID. More on this will be covered later.

```cpp
  REGISTER_USER_FUNCTIONS_AND_PROCEDURES()
  {
    REGISTER_USER_FUNCTION(add, 1);
  }
```
