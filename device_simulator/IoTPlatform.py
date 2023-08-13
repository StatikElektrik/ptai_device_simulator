import asyncio
from aiocoap import Context, Message, Code
import json

import logging

logger = logging.getLogger('IoTPlatform')

class IoTPlatform:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.server_address = "coap://" + self.hostname + ':' + self.port

    def request_provision(self, device_name, device_provision_key, device_provision_secret):
        received_token = asyncio.run(
            self.request_provision_async(device_name, device_provision_key, device_provision_secret))
        return received_token

    async def request_provision_async(self, device_name, device_provision_key, device_provision_secret):
        received_token = None

        client_context = await Context.create_client_context()
        await asyncio.sleep(2)
        try:

            provision_request = {"provisionDeviceKey": device_provision_key,
                                 "provisionDeviceSecret": device_provision_secret,
                                 "deviceName": device_name,
                                 }

            msg = Message(code=Code.POST, payload=str.encode(json.dumps(provision_request)),
                          uri=self.server_address + '/api/v1/provision')
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
        except Exception as e:
            logging.error(e)
        finally:
            await client_context.shutdown()
            return received_token

    def send_telemetry_data(self, device_token, data):
        asyncio.run(self.send_telemetry_data_async(device_token, data))

    async def send_telemetry_data_async(self, device_token, data):
        msg = Message(code=Code.POST, payload=str.encode(json.dumps(data)),
                      uri=self.server_address + ('/api/v1/%s/telemetry' % device_token))

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
            raise Exception("[THINGSBOARD CLIENT] Cannot save telemetry with received credentials!")

    def send_attribute_data(self, device_token, data):
        asyncio.run(self.send_attribute_data_async(device_token, data))

    async def send_attribute_data_async(self, device_token, data):
        msg = Message(code=Code.POST, payload=str.encode(json.dumps(data)),
                      uri=self.server_address + ('/api/v1/%s/attributes' % device_token))

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
            raise Exception("[THINGSBOARD CLIENT] Cannot save telemetry with received credentials!")
