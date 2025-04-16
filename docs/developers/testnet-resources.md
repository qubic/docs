---
title: Testnet Resources
---

# Qubic Testnet Resources

This page provides information about resources available for testing and development on the Qubic testnet.

## Testnet Faucet

Need test funds for development? You can access the Qubic faucet:

1. Join the [Qubic Discord](https://discord.gg/qubic)
2. Navigate to the `#bot-commands` channel
3. Use the faucet command to receive:
   - 1000 Qubics on mainnet
   - Test Qubics for the testnet RPC

This will provide you with the necessary funds to test your smart contracts during development.

## Available Testnet Seeds

For testing purposes, the following pre-funded seeds are available on the testnet. Each seed contains approximately 1 billion Qubic tokens.

```
fwqatwliqyszxivzgtyyfllymopjimkyoreolgyflsnfpcytkhagqii
xpsxzzfqvaohzzwlbofvqkqeemzhnrscpeeokoumekfodtgzmwghtqm
ukzbkszgzpipmxrrqcxcppumxoxzerrvbjgthinzodrlyblkedutmsy
wgfqazfmgucrluchpuivdkguaijrowcnuclfsjrthfezqapnjelkgll
kewgvatawujuzikurbhwkrisjiubfxgfqkrvcqvfvgfgajphbvhlaos
nkhvicelolicthrcupurhzyftctcextifzkoyvcwgxnjsjdsfrtbrbl
otyqpudtgogpornpqbjfzkohralgffaajabxzhneoormvnstheuoyay
ttcrkhjulvxroglycvlpgesnxpwgjgvafpezwdezworzwcfobevoacx
mvssxxbnmincnnjhtrlbdffulimsbmzluzrtbjqcbvaqkeesjzevllk
jjhikmkgwhyflqdszdxpcjrilnoxerfeyttbbjahapatglpqgctnkue
nztizdwotovhuzchctpfdgylzmsdfxlvdcpikhmptqjbwwgbxavhtwo
lxbjeczdoqyjtzhizbeapkbpvfdbgxxbdbhyfvzhbkysmgdxuzspmwu
zwoggmzfbdhuxrikdhqrmcxaqmpmdblgsdjzlesfnyogxquwzutracm
inkzmjoxytbhmvuuailtfarjgooearejunwlzsnvczcamsvjlrobsof
htvhtfjxzqandmcshkfifmrsrikrcpsxmnemcjthtmyvsqqcvwckwfk
hmsmhamftvncxcdvxytqgdihxfncarwzatpjuoecjqhceoepysozwlp
wrnohgpgfuudvhtwnuyleimplivlxcaswuwqezusyjddgkdigtueswb
fisfusaykkovsskpgvsaclcjjyfstrstgpebxvsqeikhneqaxvqcwsf
jftgpcowwnmommeplhbvgotjxrtkmiddcjmitbxoekwunmlpmdakjzq
svaluwylhjejvyjvgmqsqjcufulhusbkkujwrwfgdphdmesqjirsoep
lzinqhyvomjzqoyluifguhytcgpftdxndswbcqriecatcmfidbnmvka
mqamjotnshocvekufdqylgtdcembtddlfockjyaotfdvzqpvkylsjjk
asueorfnexvnthcuicsqqppekcdrwizxqlnkzdkazsymrotjtmdnofe
ahfulnoaeuoiurixbjygqxiaklmiwhysazqylyqhitjsgezhqwnpgql
omyxajeenkikjvihmysvkbftzqrtsjfstlmycfwqjyaihtldnetvkrw
zrfpagcpqfkwjimnrehibkctvwsyzocuikgpedchcyaotcamzaxpivq
kexrupgtmbmwwzlcpqccemtgvolpzqezybmgaedaganynsnjijfyvcn
```

You can use these seeds with the Qubic CLI to interact with your deployed smart contracts. For example:

```bash
./qubic-cli -nodeip YOUR_NODE_IP -nodeport YOUR_NODE_PORT -seed fwqatwliqyszxivzgtyyfllymopjimkyoreolgyflsnfpcytkhagqii -somecommand
```

## Testnet Nodes

The public testnet node is available at `https://testnet-rpc.qubic.org`. This node can be used for general development and testing.

For specific projects or hackathons, dedicated testnet nodes may be provided. These nodes offer isolated environments for testing smart contracts without interference from other developers.

When using a dedicated testnet node:

1. Each team's testnet node will have its own IP address and RPC endpoint
2. This allows you to call directly to your specific node
3. The testnet nodes are pre-configured to simplify the development process

## Monitoring Transactions

After deploying a smart contract to a testnet node, you can monitor real-time transaction logs using the qlogging service:

```bash
./qubic/scripts/qlogging 127.0.0.1 31841 1 2 3 4 21180000
```

This command will show real-time logs of transactions, transfers, and other events happening on your node. The output will look like:

```
EventTx #1FromId Told1 2[1] 21183461.153 QU transfer: from WTUBWAEQJHTFIEDXCJHVRXAXYBFCHAPQUPOQMGTJVGXYEBVRYTOVFHLFBCMB to MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWWD 10000QU.
Tick 21183462 doesn't generate any log
Tick 21183463 doesn't generate any log
...
[4] 21183473.153 Burn: MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWLWD burned 100000 QU
```

This is invaluable for debugging and understanding how your smart contract interacts with the network.

## Best Practices for Testnet Development

1. **Use the CLI for Initial Testing**: The Qubic CLI is the most direct way to interact with your contract
2. **Monitor Transaction Logs**: Use the qlogging service to understand what's happening with your transactions
3. **Test with Small Amounts**: Even with test funds, it's good practice to test with small amounts first
4. **Cleanup After Testing**: When using a dedicated node, clean up your deployment when finished
5. **Document Your Contract Index**: Keep track of your contract's index for future reference 