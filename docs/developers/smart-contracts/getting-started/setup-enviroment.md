---
sidebar_position: 1
---

# Setup Environment

To set up the environment for developing QUBIC smart contracts, you only need two things: `Visual Studio` and the [`Qubic Core`](https://github.com/qubic/core) repository. Simple, right?

:::info
We recommend to use [Qubic Core Lite](../resources/qubic-lite-core.md) repo instead of official Qubic Core so we can build and run the local testnet with our smart contract **directly in OS** without using VM to run the testnet.
:::

## 1. Install Visual Studio

Go to [https://visualstudio.microsoft.com/](https://visualstudio.microsoft.com/) and click the `Download Visual Studio` button.

![VS](/img/install_vs1.png)

Once downloaded, open the `Visual Studio Installer`. Select the `Desktop development with C++` workload.

![VS](/img/install_vs3.png)

Click the `Install` button. You’ll see a progress page — grab a coffee and wait for the installation to complete.

![VS](/img/install_vs4.png)

When the installation progess is completed, open the `Visual Studio`

![VS](/img/install_vs5.png)

## 2. Clone the repo

Choose `Clone a repository` and paste the following URL: `https://github.com/qubic/core.git`

![VS](/img/install_vs6.png)

Click the `Clone` button.

![VS](/img/install_vs7.png)

Once the cloning is complete, double-click on `Qubic.sln` on the right-hand side to open the QUBIC solution.

![VS](/img/install_vs11.png)

Now let’s test if everything is set up correctly by building the test project.  
Right-click on the `test` project and select `Build`.

![VS](/img/install_vs8.png)

If you see logs like the one below — congrats! You've successfully set up your development environment!

```
3>test.vcxproj -> C:\Users\admin\source\repos\core\x64\Debug\test.exe
3>C:\Users\admin\source\repos\core\test\data\custom_revenue.eoe
3>C:\Users\admin\source\repos\core\test\data\samples_20240815.csv
3>C:\Users\admin\source\repos\core\test\data\scores_v4.csv
3>C:\Users\admin\source\repos\core\test\data\scores_v5.csv
3>4 File(s) copied
3>Done building project "test.vcxproj".
========== Rebuild All: 3 succeeded, 0 failed, 0 skipped ==========
========== Rebuild completed at 1:57 PM and took 01:04.789 minutes ==========
```

![VS](/img/install_vs9.png)

:::warning
If you see the logs is The Windows SDK version xx.xx.xxxx.x was not found. Install the required version of Windows SDK or change the SDK version in the project property pages or by right-clicking the solution and selecting "Retarget solution".
:::
