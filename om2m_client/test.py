# Import the OM2MClient class from its module if it's in a separate file.
# from om2m_client import OM2MClient
from om2m_client import OM2MClient

# Configuration details
cse_ip = "10.83.2.249"
cse_port = 5684  # CoAP port
device_name = "TestDevice"
container_name = "TestContainer"
cse_type = "mn"  # MN-CSE (middle node)
credentials = "admin:admin"  # Default OM2M credentials
protocol = "COAP"  # Use CoAP protocol

# Initialize the OM2MClient
client = OM2MClient(
    cse_ip=cse_ip,
    cse_port=cse_port,
    device_name=device_name,
    container_name=container_name,
    cse_type=cse_type,
    cred=credentials,
    protocol=protocol
)

try:
    # Register the AE (Application Entity)
    print("Registering Application Entity (AE)...")
    client.register_ae()

    # Create a container under the AE
    print("Creating container...")
    client.create_container()

    # Send some example data
    example_data = {"temperature": 25.5, "humidity": 60}
    print("Sending data...")
    client.send_data(example_data)

finally:
    # Gracefully stop the client
    print("Stopping client...")
    client.stop()
