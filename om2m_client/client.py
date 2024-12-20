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

    def __init__(self, cse_url, device_name, container_name, origin='admin:admin'):
        """
        Initializes the OM2MClient with necessary configurations.
        
        :param cse_url: Base URL of the OM2M CSE (e.g., "http://10.83.2.249:8282/~/mn-cse/mn-name")
        :param device_name: Name of the device/Application Entity (AE)
        :param container_name: Name of the container to store data
        :param origin: Authorization credentials (default: 'admin:admin')
        """
        self.cse_url = cse_url.rstrip('/')
        self.device_name = device_name
        self.container_name = container_name
        self.origin = origin

        # Define AE and Container URLs
        self.ae_url = f"{self.cse_url}/{self.device_name}"
        self.container_url = f"{self.ae_url}/{self.container_name}"

        # Headers
        self.headers_ae = {
            'X-M2M-Origin': self.origin,
            'Content-Type': 'application/json;ty=2'  # ty=2 for AE
        }
        self.headers_cnt = {
            'X-M2M-Origin': self.origin,
            'Content-Type': 'application/json;ty=3'  # ty=3 for Container
        }
        self.headers_data = {
            'X-M2M-Origin': self.origin,
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
