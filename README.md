# PTAI Embedded Systems Simulator
This is a data simulator for the PTAI Embedded Systems project. It is designed to simulate the data that would be sent from the embedded system to the ThingsBoard server.
It creates a function, and creates arbitrary data with specified error rates. It then sends the data to the ThingsBoard server.

## Usage
```bash
~$ python3 main.py --function_type=[FUNCTION_TYPE] --error_rate=[ERROR_RATE] --frequency=[FREQUENCY] --duration=[DURATION]
```

### Environmental Variables
```bash
THINGSBOARD_HOST="[HOST_COAP_URL_HERE]"
THINGSBOARD_PORT="[HOST_COAP_PORT_HERE]"
DEVICE_PROVISION_KEY="[DEVICE_PROVISION_KEY_HERE]"
DEVICE_PROVISION_SECRET="[DEVICE_PROVISION_SECRET_HERE]"
```