# Call Contract Function

We can call the contract function using `qubic-cli`, but unfortunately, we still need to manually craft the packet, send it, receive the response in hex, and then decode it into a readable struct. It's a bit of a tangled process—but let's see how to get it done.

## Craft The Packet

Let's say we have a function called `GetStateNumber` in our deployed contract

<details>
<summary>Show `GetStateNumber` Function</summary>
```
struct GetStateNumber_input  {
};
struct GetStateNumber_output {
	uint64 stateNumber;
};
PUBLIC_FUNCTION(GetStateNumber) {
	output.stateNumber = state.stateNumber;
}
```
</details>

So we can create the packet with this following code (added as a test case in your test)

:::info
Remember to `#include "network_messages/contract.h"` in your test source first
:::

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

TEST(Contract, CallFunction) {
	struct {
		RequestResponseHeader	 header;
		RequestContractFunction rcf;
		// Add your input here if needed
		// Example: QNS::GetStateNumber_input input;
	} packet;

	packet.header.setSize<sizeof(packet)>();
	packet.header.randomizeDejavu();
	packet.header.setType(RequestContractFunction::type);

	// GetStateNumber doesn't expect any input, so inputSize should be 0
	// Example if you have input: packet.rcf.inputSize = sizeof(QNS::GetStateNumber_input);
	packet.rcf.inputSize		= 0;
	// In this case GetStateNumber has been registered with id = 14
	packet.rcf.inputType		= 14;
	// Change to your contract index
	packet.rcf.contractIndex	= QNS_CONTRACT_INDEX;

	// Modify the input if needed
	// Example: packet.input.stateNumber = 0; but in this case we don't need input

	unsigned char* hexStr		= new unsigned char[sizeof(packet) * 2 + 1];
	byteToHex(reinterpret_cast<const uint8_t*>(&packet), reinterpret_cast<char*>(hexStr), sizeof(packet));
	hexStr[sizeof(packet) * 2]	= '\0'; // Null-terminate the string

	cout << "Hex String: " << hexStr << endl;
	cout << "Size: " << sizeof(packet) << endl;
}
```

Example output:

```
C:\Users\Admin>C:\Users\Admin\Projects\core\x64\Release\test.exe
Running main() from D:\a\_work\1\s\ThirdParty\googletest\googletest\src\gtest_main.cc
[==========] Running 140 tests from 30 test cases.
[----------] Global test environment set-up.
[----------] 1 test from Contract
[ RUN      ] Contract.CallFunction
Hex String: 1000002ae0238c350d0000000e000000
Size: 16
```

## Call Function

Then use these as inputs for qubic cli

```bash
qubic-cli.exe -nodeip 162.120.19.25 -nodeport 31841 -sendrawpacket 1000002ae0238c350d0000000e000000 16
```

Example output

```bash
C:\Users\Admin>C:\Users\Admin\Projects\qubic-cli\Debug\qubic-cli.exe -seed ghromhommngqxjokdlnyjkaoxmjbnwqneiikevfkxfncftudczluvcl -nodeip 162.120.19.25 -nodeport 31841 -sendrawpacket 1000002ab25f5c7d0d0000000e000000 16
Received 16 bytes
1000002bb25f5c7d0000000000000000
```

Your actually response start from **bytes 8** in this case is `0000000000000000` (`stateNumber` is 0)

:::warning
You can't use the same same input hex (dejavu) more then one. You need to re-generate the input hex then send again.
:::

:::info
If your reponse is a complex struct, you should copy the hex then call `hexToByte()` then cast these bytes to pointer of the `output` struct
:::
