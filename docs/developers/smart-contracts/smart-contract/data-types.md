---
sidebar_position: 3
---

# Data Types

## Integers

Native integer types are **prohibited** in Qubic smart contracts. Instead, use the integer types provided by QPI: `sint8`, `uint8`, `sint16`, `uint16`, `sint32`, `uint32`, `sint64`, and `uint64`.

```cpp
sint8 a = 1;
uint64 b = 10000000000;
```

## Booleans

Booleans is resperent by `bit` data type

```cpp
bit isRight = true;
bit isWrong = false;
bit notSure = true & false;
```

## Id

To respersent user public key we can use the `id` data type

```cpp
id user1 = id(1,2,3,4);
id user2 = id(2,3,4,5);
```

## Array

Array of L elements of type T (L must be 2^N)

:::note
Read more about Array at `QPI::Array`
:::

```cpp
Array<uint64, 4> arr;
arr.set(0, 1);
cout << arr.get(0) << endl; // print 1
```

## BitArray

Array of L bits encoded in array of uint64 (overall size is at least 8 bytes, L must be 2^N)

:::note
Read more about BitArray at `QPI::BitArray`
:::

```cpp
BitArray<uint64, 4> arr;
arr.set(1, 0);
cout << arr.get(1) << endl; // print 0
```

## HashMap

Hash map of (key, value) pairs of type (KeyT, ValueT) and total element capacity L.

:::note
Read more about HashMap at `QPI::HashMap`
:::

```cpp
// template <typename KeyT, typename ValueT, uint64 Length>
// Length must be 2^n
HashMap<uint64, uint64, 4> map;
map.set(0, 1);

uint64 value;
map.get(0, value);

cout << value << endl; // print 1
```

## HashSet

Hash set of keys of type KeyT and total element capacity L.

:::note
Read more about HashSet at `QPI::HashSet`
:::

```cpp
// template <typename KeyT, uint64 Length>
// Length must be 2^n
HashSet<uint64, 4> set;
set.add(0);

cout << set.contains(0); // print true
```

## Collection

Collection of priority queues of elements with type T and total element capacity L.

:::note
Read more about Collection at `QPI::Collection`
:::

```cpp
// template <typename T, uint64 L>
// Length must be 2^n
Collection<uint64, 128> collection = Collection<uint64, 128>();
collection.add(id::zero(), 1, 1);
collection.add(id::zero(), 2, 2);

cout << collection.population() << endl; // print 2
cout << collection.element(collection.headIndex(id::zero())) << endl; // print 2
```
