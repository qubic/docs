---
title: Transaction Anatomy
---

# Transaction Anatomy

## Conceptual Structure

```
Transaction = {
    Source: Sender's public key
    Destination: Receiver/contract public key
    Amount: QUs to transfer
    Tick: Future execution moment
    Type: Function/procedure index to invoke
    Size: Data payload bytes
    Payload: Serialized data in base64
    Signature: Cryptographic authentication
}
```

## Input Size Calculation

**Fundamental principle**: `inputSize = sizeof(C++_input_struct)`

Understanding how to calculate the input size is crucial for creating valid transactions. The input size must exactly match the size of the C++ struct that the smart contract expects to receive. This isn't just a suggestion - it's a hard requirement for transaction validity.

```cpp
// Example: AddToBidOrder_input structure from QX contract
struct AddToBidOrder_input {
    id issuer;              // 32 bytes (256-bit identifier)
    uint64 assetName;       // 8 bytes (64-bit integer)
    sint64 price;           // 8 bytes (signed 64-bit integer)
    sint64 numberOfShares;  // 8 bytes (signed 64-bit integer)
};
// Total size: 32 + 8 + 8 + 8 = 56 bytes
```

**How to calculate correctly**:

- **Field-by-field analysis**: Examine each field in the struct and its data type size
- **Memory alignment**: C++ automatically aligns struct members to optimize memory access, which can add padding bytes
- **Platform considerations**: Most Qubic contracts assume 64-bit architecture with standard type sizes
- **Documentation verification**: Always cross-reference with official documentation or test with known working examples

**Common mistakes**:

- **Ignoring padding**: Assuming struct size is just the sum of field sizes without considering alignment
- **Wrong data types**: Confusing similar types like `uint32` vs `uint64` or `sint64` vs `uint64`
- **String handling**: Misunderstanding how text data is encoded within fixed-size fields

## Payload Serialization Process

**Data pipeline**:

```
Input data → C++ Struct → Raw bytes → Base64 encoding → Payload
```

![Data pipeline](/img/data_pipeline.png)

**Conceptual steps**:

1. **Data mapping**: Convert input parameters to struct format
2. **Binary serialization**: Respect exact C++ struct memory layout
3. **Encoding**: Convert bytes to base64 for HTTP/JSON transport
4. **Validation**: Verify size matches inputSize

## Execution Flow

### For Functions (Queries)

```
pseudocode:
1. build_payload(input_data)
2. calculate_input_size(struct_definition)
3. send_rpc_query(contractIndex, inputType, payload)
4. decode_base64_response(result)
5. parse_output_struct(response_bytes)
```

### For Procedures (Transactions)

```
pseudocode:
1. get_current_tick()
2. calculate_target_tick(current_tick + offset)
3. build_payload(input_data)
4. create_transaction(destination, type, size, payload, target_tick)
5. sign_transaction(private_key)
6. broadcast_transaction(signed_transaction)
7. verify_inclusion_in_tick(target_tick, tx_id)
8. validate_expected_effects(state_changes)
```
