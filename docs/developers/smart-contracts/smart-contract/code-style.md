---
sidebar_position: 9
---

# Smart Contract Style Guide

Smart contracts are easier to read, maintain, and audit when they follow a consistent style.  
This guide defines the conventions for naming, constants, and formatting that should be used when writing contracts, ensuring clarity and reducing errors.

## Function And Procedure Naming

Use **camelCase** for naming functions, procedures, and their input/output structures.

```cpp
struct getStateNumber_input
{
};

struct getStateNumber_output
{
    uint64 stateNumber;
};

PUBLIC_FUNCTION(getStateNumber)
{
}
```

## Constants naming

Use `ALL_CAPS` for constants in your contract.

```cpp
constexpr uint8 MYCONTRACT_VAR1 = 1;
```

## Curly Braces

Always place `{}` on a new line.

```cpp
// if-else
if (cond)
{
   // do something
}
else
{
   // do something else
}
```

```cpp
// struct
struct myStruct
{
};
```
