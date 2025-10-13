# Setup RPC

Manually setting up the RPC server can be a challenging task, but fortunately, we can use Docker to simplify the process.

## Install Docker

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="linux" label="Linux" default>
```bash
apt update
apt install -y docker.io
curl -L "https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
  </TabItem>
  <TabItem value="window" label="Windows">
```
1. Download and install the docker desktop at https://www.docker.com/products/docker-desktop.
2. Launch Docker Desktop from Start Menu.
3. Wait until it shows Docker is running.
```
  </TabItem>
</Tabs>

## Docker Compose File

Download the `docker-compose.yaml` and adjust `QUBIC_NODES_QUBIC_PEER_LIST` variable:

[Docker Compose File](https://github.com/KavataK/qubic-node-setup/blob/main/docker-compose.yaml)

## Start The Server

```bash
docker-compose up -d
```

Example output:

```bash
root@31217:~/core-docker# docker-compose up -d
[+] Running 8/8
 ✔ Container mongo-db         Running                                                                              0.0s
 ✔ Container qubic-nodes      Healthy                                                                              1.7s
 ✔ Container qubic-archiver   Started                                                                              0.0s
 ✔ Container qubic-http       Started                                                                              0.0s
 ✔ Container stats-processor  Started                                                                              0.0s
 ✔ Container traefik          Started                                                                              0.0s
 ✔ Container qubic-events     Started                                                                              0.0s
 ✔ Container stats-api        Started                                                                              0.0s
```

Your RPC is running at `IP:8000`, See [RPC Docs](https://qubic.github.io/integration/Partners/qubic-rpc-doc.html?urls.primaryName=Qubic%20RPC%20Live%20Tree) for more details.

Let's test if our RPC is running by make a GET request to `http://IP:8000/v1/tick-info`, Example output

```json
{
  "tickInfo": {
    "tick": 18480136,
    "duration": 0,
    "epoch": 170,
    "initialTick": 18480000
  }
}
```

## References

https://github.com/KavataK/QubicNetworkDeploymentGuide

https://github.com/KavataK/qubic-node-setup

https://github.com/qubic/qubic-dev-kit
