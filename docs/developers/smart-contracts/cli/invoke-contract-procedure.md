# Invoke Contract Procedure

Similar to calling a function, we can use `qubic-cli` to invoke procedures. However, we still need to manually craft the packet. Hopefully, in the future there will be tools to simplify this process.

## Get Contract Indentity

To invoke a contract procedure, we must know the contract ID. You can retrieve it by running the following script in your test:

```cpp
TEST(Contract, GetId) {
	id contract(QNS_CONTRACT_INDEX, 0, 0, 0);
	CHAR16* contractAddress = new CHAR16[61];
	getIdentity(contract.m256i_u8, contractAddress, false);
	cout << "Contract address: ";
	for (int i = 0; i < 60; i++) {
		cout << (char)contractAddress[i];
	}
	cout << endl;
}
```

Example output

```
...
==========] Running 140 tests from 30 test cases.
[----------] Global test environment set-up.
[----------] 1 test from Contract
[ RUN      ] Contract.GetId
Contract address: NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAML
...
```

## Craft The Packet

Lets say we have a procedure called `SetNumberState`

<details>
<summary>Show `SetStateNumber` Contract Function</summary>
```cpp
struct SetStateNumber_input {
	uint64	stateNumber;
};

struct SetStateNumber_output {
	uint8	result;
};

PUBLIC_PROCEDURE(SetStateNumber) {
	if (input.stateNumber < state.stateNumber) {
		output.result =1;
		return;
	}
	state.stateNumber = input.stateNumber;
	output.result = 0;
}
```
</details>

To invoke the procedure we need to prepare the hex data for `SetStateNumber_input`

```cpp
static void byteToHex(const uint8_t* byte, char* hex, const int sizeInByte)
{
	for (int i = 0; i < sizeInByte; i++)
	{
		snprintf(hex + i * 2, 3, "%02x", byte[i]);
	}
}

static void hexToByte(const char* hex, uint8_t* byte, const int sizeInByte)
{
	for (int i = 0; i < sizeInByte; i++)
	{
		sscanf(hex + i * 2, "%2hhx", &byte[i]);
	}
}

TEST(Contract, InvokeContract) {
	QNS::SetStateNumber_input input;
	input.stateNumber = 1;
	unsigned char* hexStr = new unsigned char[sizeof(input) * 2 + 1];
	byteToHex(reinterpret_cast<const uint8_t*>(&input), reinterpret_cast<char*>(hexStr), sizeof(input));
	hexStr[sizeof(input) * 2] = '\0'; // Null-terminate the string
	cout << "Hex String: " << hexStr << endl;
	cout << "Input size: " << sizeof(input) << endl;
}
```

Example output:

```bash
...
Running main() from D:\a\_work\1\s\ThirdParty\googletest\googletest\src\gtest_main.cc
[==========] Running 140 tests from 30 test cases.
[----------] Global test environment set-up.
[----------] 1 test from Contract
[ RUN      ] Contract.InvokeContract
Hex String: 0100000000000000
...
```

## Invoke Procedure

Now invoke the contract using `qubic-cli`:

```bash
qubic-cli.exe -seed <SEED> -nodeip <IP> -nodeport <PORT> -sendcustomtransaction <CONTRACT_ID> <PROCEDURE_ID> <AMOUNT> <INPUT_SIZE> <INPUT_HEX>
```

Example command:

```bash
qubic-cli.exe -seed ghromhommngqxjokdlnyjkaoxmjbnwqneiikevfkxfncftudczluvcl -nodeip 162.120.19.25 -nodeport 31841 -sendcustomtransaction NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAML 15 0 8 0100000000000000
```

Example output:

```
C:\Users\Admin>C:\Users\Admin\Projects\qubic-cli\Debug\qubic-cli.exe -seed ghromhommngqxjokdlnyjkaoxmjbnwqneiikevfkxfncftudczluvcl -nodeip 162.120.19.25 -nodeport 31841 -sendcustomtransaction NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAML 15 0 8 0100000000000000
Transaction has been sent!
~~~~~RECEIPT~~~~~
TxHash: nchougstcpxokaicxzuvbaljttdanprejaffegqragbanbwzdlelshycpjbd
From: WRHOEDJCSNSWACSNWPRQWPBXQIOCAULOEJPCUDFDDFRLALPTIQUESAIELSNA
To: NAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAML
Input type: 15
Amount: 0
Tick: 18480032
Extra data size: 8
Extra data: 0100000000000000
MoneyFlew: N/A
~~~~~END-RECEIPT~~~~~
run ./qubic-cli [...] -checktxontick 18480032 nchougstcpxokaicxzuvbaljttdanprejaffegqragbanbwzdlelshycpjbd
to check your tx confirmation status
```

Your procedure invocation is scheduled for tick `18480032`. The core node will process your procedure call and update the state when the network reaches that tick.

After the procedure is processed, try calling the `GetStateNumber` function again to verify whether the state was actually updated.

```bash
C:\Users\Admin>qubic-cli.exe -seed ghromhommngqxjokdlnyjkaoxmjbnwqneiikevfkxfncftudczluvcl -nodeip 162.120.19.25 -nodeport 31841 -sendrawpacket 1000002ab25f5c7d0d0000000e000000 16
Sent 16 bytes
Received 16 bytes
1000002bb25f5c7d0100000000000000
```

If we remove the first 8 bytes, we get `0100000000000000`, which is `1` in decimal (Little Endian) — just as we expected.

:::warning
You must use a seed with balance to successfully invoke the procedure. Also, adjust `<AMOUNT>` if your contract requires a fee or cost.
:::

:::info
There's a key difference between calling a function and invoking a procedure. Calling a procedure actually creates a custom transaction that sends Qubic to the contract address. The core will then schedule your procedure to run when the network reaches the tick which your transaction lives

On the other hand, calling a function simply opens a TCP connection, asks the node to run the function, and returns the output immediately.

tl;dr: Function calls are executed **immediately**, procedures **are not**.
:::
