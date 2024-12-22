# om2m_client/client.py

import urequests as requests
import ujson as json
import sys

from .exceptions import OM2MError

class OM2MClient:
    """
    A client for interacting with an OM2M CSE.
    Handles AE registration, container creation, and data transmission.
    """

    def __init__(self, cse_ip, device_name, container_name, cse_port=8282, cse_type="mn", cred="admin:admin"):
        """
        Initializes the OM2MClient with necessary configurations.
        
        :param cse_ip: IP address of the OM2M CSE (e.g., "10.83.2.249")
        :param device_name: Name of the device/Application Entity (AE)
        :param container_name: Name of the container to store data
        :param cse_port: Port number for the CSE (default: 8282)
        :param cse_name: Path to the CSE name (default: "mn-cse/mn-name")
        :param cred: Authorization credentials (default: 'admin:admin')
        """
        self.cse_ip = cse_ip
        self.cse_port = cse_port
        self.cse= cse_type + "-cse"
        self.cse_name = cse_type + "-name"
        self.device_name = device_name
        self.cse_type = cse_type
        self.container_name = container_name
        self.cred = cred

        # Construct the CSE URL
        self.cse_url = f"http://{self.cse_ip}:{self.cse_port}/~/" + self.cse_name
        # Define AE and Container URLs
        self.ae_url = f"{self.cse_url}/{self.device_name}"
        self.container_url = f"{self.ae_url}/{self.container_name}"

        # Headers
        self.headers_ae = {
            'X-M2M-Origin': self.cred,
            'Content-Type': 'application/json;ty=2'  # ty=2 for AE
        }
        self.headers_cnt = {
            'X-M2M-Origin': self.cred,
            'Content-Type': 'application/json;ty=3'  # ty=3 for Container
        }
        self.headers_data = {
            'X-M2M-Origin': self.cred,
            'Content-Type': 'application/json;ty=4'  # ty=4 for ContentInstance
        }

    def register_ae(self):
        """
        Registers the Application Entity (AE) with the OM2M CSE.
        """
        payload = {
            "m2m:ae": {
                "rn": self.device_name,
                "api": f"{self.device_name}_api",
                "rr": True,
                "lbl": [self.device_name]
            }
        }
        try:
            response = requests.post(self.cse_url, headers=self.headers_ae, json=payload)
            if response.status_code == 201:
                print("[OM2M] AE registered successfully.")
            elif response.status_code == 409:
                print("[OM2M] AE already exists.")
            else:
                raise OM2MError(f"Failed to register AE. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            raise OM2MError(f"Exception during AE registration: {e}")

    def create_container(self):
        """
        Creates a container under the AE if it doesn't already exist.
        """ 
        payload = {
            "m2m:cnt": {
                "rn": self.container_name
            }
        }
        try:
            # Check if the container already exists
            check_response = requests.get(self.container_url, headers=self.headers_cnt)
            if check_response.status_code == 200:
                print("[OM2M] Container already exists.")
                return

            # Create the container if it does not exist
            response = requests.post(self.ae_url, headers=self.headers_cnt, json=payload)
            if response.status_code == 201:
                print("[OM2M] Container created successfully.")
            elif response.status_code == 409:
                print("[OM2M] Container already exists.")
            else:
                raise OM2MError(f"Failed to create container. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            raise OM2MError(f"Exception during container creation: {e}")

    def create_descriptor(self):
        """
        Creates a container under the AE if it doesn't already exist.
        """
        payload = {
            "m2m:cnt": {
                "rn": "DESCRIPTOR"
            }
        }
        try:
            response = requests.post(self.ae_url, headers=self.headers_cnt, json=payload)
            if response.status_code == 201:
                print("[OM2M] Descriptor created successfully.")
            elif response.status_code == 409:
                print("[OM2M] Descriptor already exists.")
            else:
                raise OM2MError(f"Failed to create Descriptor. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            raise OM2MError(f"Exception during Descriptor creation: {e}")

    def send_data(self, data):
        """
        Sends sensor data to the OM2M server.

        :param data: A dictionary containing the sensor data.
        """
        payload = {
            "m2m:cin": {
                "cnf": "application/json",
                "con": json.dumps(data)
            }
        }
        try:
            response = requests.post(self.container_url, headers=self.headers_data, json=payload)
            if response.status_code in (200, 201, 202):
                print("[OM2M] Data uploaded successfully.")
            else:
                raise OM2MError(f"Failed to upload data. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            raise OM2MError(f"Exception during data upload: {e}")
