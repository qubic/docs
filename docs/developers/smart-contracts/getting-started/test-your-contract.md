---
sidebar_position: 3
---

# Test Your Contract

Now that we’ve created our contract, it's time to test it and make sure it works as expected.

## Create test program

> Test program should be named as `contract_[your_contract_name_lowercase].cpp`.

> Example: For a contract named `MyTest`, the test program should be `contract_mytest.cpp`.

Navigate to the `test` project and create a new program called `contract_mytest.cpp` with the following template:

```cpp title="contract_mytest.cpp"
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

## Build the test

Right-click the test project in Visual Studio and select Build. If successful, you’ll see output like this:

```
...
...
1>Generating Code...
1>test.vcxproj -> C:\Users\admin\source\repos\core\x64\Debug\test.exe
1>C:\Users\admin\source\repos\core\test\data\custom_revenue.eoe
1>C:\Users\admin\source\repos\core\test\data\samples_20240815.csv
1>C:\Users\admin\source\repos\core\test\data\scores_v4.csv
1>C:\Users\admin\source\repos\core\test\data\scores_v5.csv
1>4 File(s) copied
1>Done building project "test.vcxproj".
========== Build: 1 succeeded, 0 failed, 2 up-to-date, 0 skipped ==========
========== Build completed at 2:44 PM and took 29.164 seconds ==========
```

You can now run the test executable via Command Prompt:

```cpp
C:\Users\admin>C:\Users\admin\source\repos\core\x64\Debug\test.exe
Running main() from D:\a\_work\1\s\ThirdParty\googletest\googletest\src\gtest_main.cc
[==========] Running 216 tests from 39 test cases.
[----------] Global test environment set-up.
[----------] 3 tests from TestCoreAssets
[ RUN      ] TestCoreAssets.CheckLoadFile
```

As you can see, your test is not executed first. Waiting for other tests can waste time — but there's a quick trick to prioritize yours.

## How To Run Your Test First

**1. Unload the Project**

-   Right click the `test` project then choose `Unload project`

**2. Edit the Project File**

-   Right-click the unloaded project → Edit Project File
-   Find the section like this:

```xml title="test.vcxproj"
...
  <ItemGroup>
    <ClCompile Include="assets.cpp" />
    <ClCompile Include="common_def.cpp" />
    <ClCompile Include="contract_core.cpp" />
    <ClCompile Include="contract_msvault.cpp" />
    <ClCompile Include="contract_mytest.cpp" />
    <ClCompile Include="contract_qearn.cpp" />
    <ClCompile Include="contract_qutil.cpp" />
    <ClCompile Include="contract_qx.cpp" />
    <ClCompile Include="contract_qvault.cpp" />
    <ClCompile Include="contract_testex.cpp" />
    <ClCompile Include="contract_qbay.cpp" />
    <ClCompile Include="contract_gqmprop.cpp" />
    <ClCompile Include="custom_mining.cpp" />
    <ClCompile Include="file_io.cpp" />
    <ClCompile Include="qpi_collection.cpp" />
    <ClCompile Include="qpi_hash_map.cpp" />
    <ClCompile Include="kangaroo_twelve.cpp" />
    <ClCompile Include="revenue.cpp" />
    <ClCompile Include="spectrum.cpp" />
    <ClCompile Include="stdlib_impl.cpp" />
    <ClCompile Include="time.cpp" />
    <ClCompile Include="tx_status_request.cpp" />
    <ClCompile Include="m256.cpp" />
    <ClCompile Include="math_lib.cpp" />
    <ClCompile Include="network_messages.cpp" />
    <ClCompile Include="platform.cpp" />
    <ClCompile Include="qpi.cpp" />
    <ClCompile Include="score.cpp" />
    <ClCompile Include="score_cache.cpp" />
    <ClCompile Include="tick_storage.cpp" />
    <ClCompile Include="virtual_memory.cpp" />
    <ClCompile Include="vote_counter.cpp" />
  </ItemGroup>
...
```

**3. Move Your Test File to the Top**

Move the contract_mytest.cpp entry above all other files, like so:

```xml title="test.vcxproj"
...
  <ItemGroup>
    <ClCompile Include="contract_mytest.cpp" />
    <ClCompile Include="assets.cpp" />
    <ClCompile Include="common_def.cpp" />
    <ClCompile Include="contract_core.cpp" />
    <ClCompile Include="contract_msvault.cpp" />
    <ClCompile Include="contract_qearn.cpp" />
    <ClCompile Include="contract_qutil.cpp" />
    <ClCompile Include="contract_qx.cpp" />
    <ClCompile Include="contract_qvault.cpp" />
    <ClCompile Include="contract_testex.cpp" />
    <ClCompile Include="contract_qbay.cpp" />
    <ClCompile Include="contract_gqmprop.cpp" />
    <ClCompile Include="custom_mining.cpp" />
    <ClCompile Include="file_io.cpp" />
    <ClCompile Include="qpi_collection.cpp" />
    <ClCompile Include="qpi_hash_map.cpp" />
    <ClCompile Include="kangaroo_twelve.cpp" />
    <ClCompile Include="revenue.cpp" />
    <ClCompile Include="spectrum.cpp" />
    <ClCompile Include="stdlib_impl.cpp" />
    <ClCompile Include="time.cpp" />
    <ClCompile Include="tx_status_request.cpp" />
    <ClCompile Include="m256.cpp" />
    <ClCompile Include="math_lib.cpp" />
    <ClCompile Include="network_messages.cpp" />
    <ClCompile Include="platform.cpp" />
    <ClCompile Include="qpi.cpp" />
    <ClCompile Include="score.cpp" />
    <ClCompile Include="score_cache.cpp" />
    <ClCompile Include="tick_storage.cpp" />
    <ClCompile Include="virtual_memory.cpp" />
    <ClCompile Include="vote_counter.cpp" />
  </ItemGroup>
...
```

**4. Save and Reload**

-   Save the .vcxproj file.
-   Right-click the project → Reload Project

Now, rebuild and run the test again. You should see your test run first:

```cpp
...
[==========] Running 216 tests from 39 test cases.
[----------] Global test environment set-up.
[----------] 1 test from MyTest
[ RUN      ] MyTest.TestAdd
[       OK ] MyTest.TestAdd (36761 ms)
[----------] 1 test from MyTest (36780 ms total)
...
```

:::info
Since compiling tests for other contracts can be heavy—and we only want to test our own contract—you can remove lines starting with `contract_xxx.cpp` (e.g., `contract_qearn.cpp`, `contract_msvault.cpp`) in `test.vcxproj`.
:::
