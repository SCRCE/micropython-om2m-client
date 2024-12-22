# MicroPython OM2M Client

**Work in Progress**: This package is in the early stages of development and may contain bugs and missing features.

A lightweight OM2M client for MicroPython to interact with a CSE server.
### NOTE: DESIGNED TO ONLY WORK WITH MIDDLE NODES.

## Features
- Register an Application Entity (AE)
- Create Containers under the AE
- Send sensor data to OM2M CSE servers

## Installation
Install via `upip`:
upip.install("micropython-om2m-client")
## Usage
```python
from om2m_client import OM2MClient



client = OM2MClient(
    cse_ip="180.27.251.7"
    cse_port="8282"
    cse_type="mn"
    cred="admin:admin"
    device_name="MyDevice",
    container_name="MyContainer"
)

client.register_ae()
client.create_descriptor()
client.create_container()
client.send_data({"key": "value"})
```