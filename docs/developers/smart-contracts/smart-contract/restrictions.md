---
sidebar_position: 2
---

# Restrictions of C++ Language Features

Qubic enforces strict coding rules to ensure determinism, security, and network-wide consistency. Below is a list of forbidden language features and why they are restricted:

| Prohibited Feature                       | Reason                                                                                                                                                   |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local variables on the stack             | Avoids nondeterministic memory layouts. Use `_WITH_LOCALS` macros or store data in contract state.                                                       |
| Pointers (`*`, casting, dereferencing)   | Unsafe and non-deterministic. Only allowed for multiplication.                                                                                           |
| Array brackets (`[ ]`)                   | Prevents unchecked buffer access and low-level arrays, which can lead to memory issues.                                                                  |
| Preprocessor directives (`#`)            | Disallowed to avoid hidden logic and platform-specific behavior. `#include "qpi.h"` is allowed only temporarily for IntelliSense.                        |
| Floating-point types (`float`, `double`) | Arithmetic is not deterministic across platforms.                                                                                                        |
| Division (`/`) and modulo (`%`)          | Division by zero may cause inconsistent behavior. Use `div()` and `mod()` instead, which return 0 safely.                                                |
| Strings (`"`) and chars (`'`)`           | Can lead to memory access violations or random memory jumps.                                                                                             |
| Variadic arguments (`...`)               | Compiler-dependent and unsafe for auditing.                                                                                                              |
| Double underscores (`__`)                | Reserved for internal use; may conflict with system symbols.                                                                                             |
| `QpiContext`, `const_cast`               | Can be misused to alter internal contract behavior.                                                                                                      |
| Scope resolution (`::`)                  | Only allowed for structs, enums, and namespaces inside contracts or `qpi.h`.                                                                             |
| `typedef`, `union`                       | Reduces code clarity and may be used to obscure logic or manipulate memory.                                                                              |
| Global variables                         | Disallowed to avoid shared mutable state. Global constants must be prefixed with the contract state struct name.                                         |
| Recursion / deep call nesting            | Limited to 10 levels to ensure execution is bounded and safe.                                                                                            |
| Complex types in input/output            | Only simple types (`sint`, `uint`, `bit`, `id`, `Array`, `BitArray`) are allowed. Complex types like `Collection` are banned to ensure consistent state. |
