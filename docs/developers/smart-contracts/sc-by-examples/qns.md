# Qubic Name Service

[**Source Code**](https://github.com/hackerby888/qubic-sc-examples/tree/qubic-name-service)

:::warning
This QNS contract is only for reference only and it's not the QNS contract that being developed in Qubic Eco System
:::

## Qubic Name Service (QNS) Contract Documentation

### Overview

The QNS contract is a decentralized naming system built on the Qubic blockchain that maps human-readable names to machine-readable identifiers like Qubic addresses. It provides functionality similar to DNS but with blockchain-based ownership and resolution.

### Key Features

- Domain registration and renewal system

- Subdomain management

- Address resolution (QUBIC addresses)

- Text record storage (for metadata)

- Transferable domain ownership

- Time-based domain expiration

### Data Structures

#### UEFIString

```cpp
template <uint64 LENGTH = QNS_MAX_NAME_LENGTH>
struct UEFIString : public Array<sint8, LENGTH> {
    bool isEmpty();
    bool validate();
    static UEFIString getEmpty();
    bool operator==(const UEFIString& other) const;
}
```

- Fixed-length string type for domain names

- Validation ensures proper format (alphanumeric, null-terminated)

- Length constraints: min 1, max 32 chars

#### Domain

```cpp
struct Domain {
    UEFIString<> subDomain;
    UEFIString<> rootDomain;
    UEFIString<QNS_MAX_TLD_LENGTH> tld;

    bool validate();
    uint64 getFullHashedValue() const;
    uint64 getRootHashedvalue() const;
}
```

- Represents a complete domain name with:

  - **subDomain**: Optional subdomain (e.g., "sub" in "sub.example.qubic")
  - **rootDomain**: Main domain name (e.g., "example" in "example.qubic")
  - **tld**: Top-level domain (e.g., "qubic")

- Provides hashing functions for efficient storage and lookup

#### RegistryRecord

```cpp
struct RegistryRecord {
    id owner;
    uint32 registerDate;
    uint16 registerEpoch;
    uint16 registrationYears;
}
```

Stores domain registration information:

- **owner**: Qubic ID of domain owner

- **registerDate**: Unix timestamp of registration

- **registerEpoch**: Qubic epoch of registration

- **registrationYears**: Number of years registered for

#### ResolveData

```cpp
struct ResolveData {
    id address;
    UEFIString<> text;
}
```

Stores resolution data for domains:

- **address**: Mapped Qubic address

- **text**: Arbitrary text record (for metadata)

## Contract State

### TLD Management

- **QUBIC_TLD**: Predefined ".qubic" TLD

- **QNS_TLD**: Predefined ".qns" TLD

- **TLDs**: Array of supported TLDs

### Storage

- **registry**: Hash map storing domain registration records

- **resolveData**: Nested hash map storing resolution data (supports subdomains)

```cpp
// Supported TLDs
UEFIString<QNS_MAX_TLD_LENGTH> QUBIC_TLD;  // ".qubic"
UEFIString<QNS_MAX_TLD_LENGTH> QNS_TLD;    // ".qns"
Array<UEFIString<QNS_MAX_TLD_LENGTH>, 2> TLDs;

// Domain registry
HashMap<uint64, RegistryRecord, QNS_MAX_NUMBER_OF_DOMAINS> registry;

// Resolution data
HashMap<uint64, HashMap<uint64, ResolveData, QNS_MAX_NUMBER_OF_SUBDOMAINS>, QNS_MAX_NUMBER_OF_DOMAINS> resolveData;
```

## Core Functions

### Registration

**`RegisterDomain`**

```cpp
struct RegisterDomain_input {
    Domain domain;
    uint16 registrationYears;
};
struct RegisterDomain_output {
    uint8 result; // QNSError code
};
```

- Registers new domain for specified years

- Validates name format and TLD

- Requires payment (2M QU/year)

### Resolution

**`SetResolveAddressData`**

```cpp
struct SetResolveAddressData_input {
    Domain domain;
    id address;
};
```

- Maps domain to Qubic address

- Owner-only operation

**`GetResolveAddressData`**

```cpp
struct GetResolveAddressData_output {
    uint8 result;
    id address;
};
```

- Returns mapped address for domain

### Management

**`RenewDomain`**

```cpp
struct RenewDomain_input {
    Domain domain;
    uint16 yearsToRenew;
};
struct RenewDomain_output {
    uint8 result;
};
```

- Extends registration period

- Additional payment required

**`TransferDomain`**

```cpp
struct TransferDomain_input {
    Domain domain;
    id newOwner;
};
struct TransferDomain_output {
    uint8 result;
};
```

- Transfers ownership to new address

- Requires 100 QU transfer fee

## System Procedure

### `INITIALIZE`

- Sets up default TLDs (.qubic, .qns)

- Initializes empty data structures

### `BEGIN_EPOCH`

- Processes domain expirations

- Cleans up stale data

- Runs automatically each epoch

## Security Notes

- All modifications require owner authorization

- Payments verified before processing

- Automatic expiration prevents squatting

- Input validation on all operations
