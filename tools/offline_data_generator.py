# To overcome the parent package problems, do not change the lines 2 and 3.
import sys
sys.path.append(sys.path[0] + "/..")

# Import argparse to read the command line arguments.
import argparse
parser = argparse.ArgumentParser(description="Offline data generator for the simulated device.")
parser.add_argument("--sensor", type=str, help="The sensor type, possible values are: 'exponantial'.", required=True)
parser.add_argument("--buffer", type=int, help="The buffer size of the data generator.", required=True)
parser.add_argument("--fsettings", type=str, help="The settings of the data generator.", required=True)
args = parser.parse_args()

# Get the arguments.
SENSOR_TYPE = args.sensor
BUFFER_SIZE = args.buffer

if SENSOR_TYPE == "exponantial":
    # Spilt the settings with comma.
    args.fsettings = args.fsettings.split(",")
    for index, value in enumerate(args.fsettings):
        if index == 0:
            BASE = float(value)
        elif index == 1:
            OFFSET = float(value)
        elif index == 2:
            SHIFT = float(value)
else:
    raise NotImplementedError(f"Sensor type {SENSOR_TYPE} is not supported.")

# Import all the core modules.
from core import DataGenerator, Device

# Create a data generator function.
sensor = DataGenerator(BUFFER_SIZE, SENSOR_TYPE, {"base": BASE, "offset": OFFSET, "shift": SHIFT})

    # Create formatted data to be sent to the ThingSpeak.
data_packet = Device.get_formatted_data(
    "sensor_data", sensor.generate(1, 25),
)

print(data_packet)