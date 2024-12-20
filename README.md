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
    cse_url="http://example.com",
    device_name="MyDevice",
    container_name="MyContainer"
)

client.register_ae()
client.create_container()
client.send_data({"key": "value"})
```