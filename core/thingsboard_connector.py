"""
This module is responsible for communication with Thingsboard IoT platform.
"""
import asyncio
import json
import logging

from aiocoap import Context, Message, Code
from typing import Any

# Create a logger interface.
logger = logging.getLogger(__name__)


class ThingsboardConnector:
    """This class is responsible for communication with Thingsboard IoT platform."""
    # @TODO: Clean up this class for its async methods.
    # They must follow the best practices for Python.

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = str(port)
        self.server_address = "coap://" + self.hostname + ":" + self.port

    def request_provision(
        self, device_name: str, provision_key: str, provision_secret: str
    ) -> str:
        """It requests a device token from Thingsboard.

        Parameters
        ----------
        device_name : str
            The name of the device.
        provision_key : str
            Device provision key.
        provision_secret : str
            Device provision secret.

        Returns
        -------
        str
            The device token.
        """
        return asyncio.run(
            self._request_provision_async(device_name, provision_key, provision_secret)
        )

    def send_telemetry_data(self, device_token: str, data: Any) -> None:
        """It sends telemetry data to Thingsboard.

        Parameters
        ----------
        device_token : str
            The device token.
        data : Any
            The data to be sent.
        """
        asyncio.run(self._send_telemetry_data_async(device_token, data))

    def send_attribute_data(self, device_token: str, data: Any) -> None:
        """It sends attribute data to Thingsboard.

        Parameters
        ----------
        device_token : str
            The device token.
        data : Any
            The data to be sent.
        """
        asyncio.run(self._send_attribute_data_async(device_token, data))

    async def _request_provision_async(
        self, device_name, device_provision_key, device_provision_secret
    ):
        received_token = None

        client_context = await Context.create_client_context()
        await asyncio.sleep(2)
        try:
            provision_request = {
                "provisionDeviceKey": device_provision_key,
                "provisionDeviceSecret": device_provision_secret,
                "deviceName": device_name,
            }

            msg = Message(
                code=Code.POST,
                payload=str.encode(json.dumps(provision_request)),
                uri=self.server_address + "/api/v1/provision",
            )
            request = client_context.request(msg)
            try:
                response = await asyncio.wait_for(request.response, 60000)
            except asyncio.TimeoutError:
                raise Exception("Request timed out!")

            if response is None:
                raise Exception("Response is empty!")

            decoded_response = json.loads(response.payload)
            logging.info("Received response: %s", decoded_response)
            received_token = decoded_response.get("credentialsValue")
            if received_token is None:
                logging.error("Failed to get access token from response.")
                logging.error(decoded_response.get("errorMsg"))
        except Exception as error:
            logging.error(error)
            raise error
        finally:
            await client_context.shutdown()
            return received_token

    async def _send_telemetry_data_async(self, device_token, data):
        msg = Message(
            code=Code.POST,
            payload=str.encode(json.dumps(data)),
            uri=self.server_address + ("/api/v1/%s/telemetry" % device_token),
        )

        client_context = await Context.create_client_context()
        await asyncio.sleep(2)

        request = client_context.request(msg)
        try:
            response = await asyncio.wait_for(request.response, 60000)
        except asyncio.TimeoutError:
            raise Exception("Request timed out!")
        finally:
            await client_context.shutdown()

        if response:
            logging.info("[THINGSBOARD CLIENT] Response from Thingsboard.")
            logging.info(response)
        else:
            raise Exception(
                "[THINGSBOARD CLIENT] Cannot save telemetry with received credentials!"
            )

    async def _send_attribute_data_async(self, device_token, data):
        msg = Message(
            code=Code.POST,
            payload=str.encode(json.dumps(data)),
            uri=self.server_address + ("/api/v1/%s/attributes" % device_token),
        )

        client_context = await Context.create_client_context()
        await asyncio.sleep(2)

        request = client_context.request(msg)
        try:
            response = await asyncio.wait_for(request.response, 60000)
        except asyncio.TimeoutError:
            raise Exception("Request timed out!")
        finally:
            await client_context.shutdown()

        if response:
            logging.info("[THINGSBOARD CLIENT] Response from Thingsboard.")
            logging.info(response)
        else:
            raise Exception(
                "[THINGSBOARD CLIENT] Cannot save telemetry with received credentials!"
            )
