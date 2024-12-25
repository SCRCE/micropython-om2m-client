# OM2M Python Client Documentation

This README provides a step-by-step guide to using the OM2M Python client to interact with an OM2M MN-CSE (Middle Node Common Services Entity). The code demonstrates creating and managing resources such as `Application Entities (AE)`, `Containers`, `ContentInstances`, and `Subscriptions`.

## Prerequisites

1. Ensure you have an OM2M MN-CSE server running and accessible.
2. Install the `om2m-client` library:
   ```bash
   pip install micropython-om2m-client
   ```
3. Adjust the `base_url` and credentials to match your MN-CSE setup.

## Example Steps

### Step 1: Initialize the OM2M Client

Initialize the client with the base URL, CSE ID, CSE name, and authentication credentials.

```python
from om2m_client.client import OM2MClient

client_mn = OM2MClient(
    base_url="http://127.0.0.1:8282",  # Adjust to your MN-CSE base URL
    cse_id="mn-cse",                  # MN-CSE identifier
    cse_name="mn-name",               # MN-CSE resource name
    username="admin",                 # Authentication username
    password="admin",                 # Authentication password
    use_json=True                     # Use JSON for data exchange
)
```

### Step 2: Create an Application Entity (AE)

Create an `AE` under the MN-CSE with specific properties.

```python
from om2m_client.models import AE

mn_ae = AE(
    rn="MY_GATEWAY_SENSOR5",            # Resource Name
    api="mn-sensor-app5",               # Application Identifier
    rr=False,                          # Request Reachability
    lbl=["Type/gatewaySensor", "Location/factory"]
)
ae_resource_id = client_mn.create_ae(mn_ae)
print("AE Resource ID (MN-CSE):", ae_resource_id)
```

### Step 3: Create a Container

Create a `Container` under the previously created `AE`.

```python
from om2m_client.models import Container

container_path = f"/{client_mn.cse_id}/{client_mn.cse_name}/{mn_ae.rn}"
mn_container = Container(
    rn="DATA",                         # Container Name
    lbl=["Category/temperature", "Unit/celsius"]
)
container_resource_id = client_mn.create_container(container_path, mn_container)
print("Container Resource ID (MN-CSE):", container_resource_id)
```

### Step 4: Add a ContentInstance

Add a `ContentInstance` under the `Container` to store sensor data.

```python
from om2m_client.models import ContentInstance

cin_path = f"{container_path}/DATA"
mn_cin = ContentInstance(
    cnf="application/json",            # Content Format
    con="{\"temperature\": 27}"        # Content (JSON string)
)
cin_resource_id = client_mn.create_content_instance(cin_path, mn_cin)
print("ContentInstance Resource ID (MN-CSE):", cin_resource_id)
```

### Step 5: Discover Resources by Label

Retrieve resources matching a specific label, such as "Type/gatewaySensor".

```python
discovery_response = client_mn.discover_resources_by_label("Type/gatewaySensor")
print("Discovery Response (MN-CSE):")
print(discovery_response)
```

### Step 6: Create a Subscription

Create a `Subscription` to receive notifications on changes to the `DATA` container.

```python
from om2m_client.models import Subscription

subscription_path = f"{container_path}/DATA"
mn_subscription = Subscription(
    rn="MY_DATA_SUB",                  # Subscription Name
    nu="http://localhost:1400/monitor", # Notification URI (local listener required)
    nct=2                              # Notification Content Type
)
subscription_resource_id = client_mn.create_subscription(subscription_path, mn_subscription)
print("Subscription Resource ID (MN-CSE):", subscription_resource_id)
```

### Step 7: Retrieve and Print Resources

Retrieve and print the `AE` and `Container` content.

#### Retrieve AE Resource

```python
retrieved_ae = client_mn.retrieve_resource(f"/{client_mn.cse_id}/{client_mn.cse_name}/MY_GATEWAY_SENSOR")
print("Retrieved AE Content (MN-CSE):")
print(retrieved_ae)
```

#### Retrieve Container Content

```python
retrieved_data = client_mn.retrieve_resource(cin_path)
print("Retrieved DATA Container Content (MN-CSE):")
print(retrieved_data)
```

## Notes

- Replace placeholders such as `base_url`, `cse_id`, `cse_name`, `username`, and `password` with your actual OM2M server details.
- Ensure your OM2M server is correctly configured to allow the operations in this example.
- The example assumes the MN-CSE uses JSON for communication.

This example serves as a template for integrating and managing resources using OM2M and Python. Customize it as needed for your specific use case.