#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import random
import time
import sys
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import re
from sense_hat import SenseHat

sense = SenseHat()

# HTTP options
# Because it can poll "after 9 seconds" polls will happen effectively
# at ~10 seconds.
# Note that for scalabilty, the default value of minimumPollingTime
# is 25 minutes. For more information, see:
# https://azure.microsoft.com/documentation/articles/iot-hub-devguide/#messaging
TIMEOUT = 241000
MINIMUM_POLLING_TIME = 9

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

RECEIVE_CONTEXT = 0
MESSAGE_COUNT = 0
MESSAGE_SWITCH = True
TWIN_CONTEXT = 0
SEND_REPORTED_STATE_CONTEXT = 0
METHOD_CONTEXT = 0
TEMPERATURE_ALERT = 30.0

# global counters
RECEIVE_CALLBACKS = 0
SEND_CALLBACKS = 0
TWIN_CALLBACKS = 0
SEND_REPORTED_STATE_CALLBACKS = 0
METHOD_CALLBACKS = 0

# chose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT

# String containing Hostname, Device Id & Device Key in the format:
# "HostName=<host_name>;DeviceId=<device_id>;SharedAccessKey=<device_key>"

if len(sys.argv) < 2:
    print("You need to provide the device connection string as command line arguments.")
    sys.exit(0)

def is_correct_connection_string():
    m = re.search("HostName=.*;DeviceId=.*;", CONNECTION_STRING)
    if m:
        return True
    else:
        return False

CONNECTION_STRING = sys.argv[1]
power_readings = sys.argv[2]

if not is_correct_connection_string():
    print("Device connection string is not correct.")
    sys.exit(0)


def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print("Confirmation[%d] received for message with result = %s" % (user_context, result))
    map_properties = message.properties()
    print("    message_id: %s" % message.message_id)
    print("    correlation_id: %s" % message.correlation_id)
    key_value_pair = map_properties.get_internals()
    print("    Properties: %s" % key_value_pair)
    SEND_CALLBACKS += 1
    print("    Total calls confirmed: %d" % SEND_CALLBACKS)


def send_reported_state_callback(status_code, user_context):
    global SEND_REPORTED_STATE_CALLBACKS
    print("Confirmation for reported state received with:\nstatus_code = [%d]\ncontext = %s" % (status_code, user_context))
    SEND_REPORTED_STATE_CALLBACKS += 1
    print("    Total calls confirmed: %d" % SEND_REPORTED_STATE_CALLBACKS)


def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    client.set_option("product_info", "HappyPath_RaspberryPi-Python")
    if client.protocol == IoTHubTransportProvider.HTTP:
        client.set_option("timeout", TIMEOUT)
        client.set_option("MinimumPollingTime", MINIMUM_POLLING_TIME)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    return client


def print_last_message_time(client):
    try:
        last_message = client.get_last_message_receive_time()
        print("Last Message: %s" % time.asctime(time.localtime(last_message)))
        print("Actual time : %s" % time.asctime())
    except IoTHubClientError as iothub_client_error:
        if iothub_client_error.args[0].result == IoTHubClientResult.INDEFINITE_TIME:
            print("No message received")
        else:
            print(iothub_client_error)


def iothub_client_sample_run(current_energy_generation):
    try:
        client = iothub_client_init()

        if client.protocol == IoTHubTransportProvider.MQTT:
            print("IoTHubClient is reporting state")
            reported_state = "{\"newState\":\"standBy\"}"
            client.send_reported_state(reported_state, len(reported_state), send_reported_state_callback, SEND_REPORTED_STATE_CONTEXT)
        # while True:
        global MESSAGE_COUNT
        # send a few messages every minute
        print("IoTHubClient sending %d messages" % MESSAGE_COUNT)
        msg_txt_formatted = str(current_energy_generation)
        message = IoTHubMessage(msg_txt_formatted)
        # optional: assign ids
        message.message_id = "message_%d" % MESSAGE_COUNT
        message.correlation_id = "correlation_%d" % MESSAGE_COUNT
        # optional: assign properties
        prop_map = message.properties()
        prop_map.add("telemetryType", "powerGeneration")

        client.send_event_async(message, send_confirmation_callback, MESSAGE_COUNT)
        print("IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % MESSAGE_COUNT)

        status = client.get_send_status()
        print("Send status: %s" % status)
        MESSAGE_COUNT += 1

        # for some reason without this sleep message wouldn't be delivered
        time.sleep(1)

    except IoTHubError as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")

    print_last_message_time(client)

X = [255, 0, 0]  # Red
O = [255, 255, 255]  # White

question_mark = [
O, O, O, X, X, O, O, O,
O, O, X, O, O, X, O, O,
O, O, O, O, O, X, O, O,
O, O, O, O, X, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, O, O, O, O
]

Empty = [0, 0, 0]
Red = [255, 0, 0]



# sense.set_pixels(question_mark)

power_display_0 = []
power_display_1 = []
power_display_2 = []

for i in range(8):
    for j in range(8):
        power_display_0.append(Empty)
        power_display_2.append(Red)
        if i > 1 and i < 6 and j > 1 and j < 6:
            power_display_1.append(Red)
        else:
            power_display_1.append(Empty)

def simulate_power_generation():
    current_energy_generation = 0
    value_changed = False
    while True:
        if value_changed:
            value_changed = False
            sense.clear()
            if current_energy_generation == 0:
                 sense.set_pixels(power_display_0)
            elif current_energy_generation == 1:
                 sense.set_pixels(power_display_1)
            else:
                 sense.set_pixels(power_display_2)
            iothub_client_sample_run(current_energy_generation)

        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "up" and current_energy_generation < 2:
                    current_energy_generation = current_energy_generation + 1
                    value_changed = True
                elif event.direction == "down" and current_energy_generation > 0:
                    current_energy_generation = current_energy_generation - 1
                    value_changed = True
                # elif event.direction == "left" and current_energy_generation != 0:
                #     current_energy_generation = 0
                #     value_changed = True
                # elif event.direction == "right" and current_energy_generation != 2:
                #     current_energy_generation = 2
                #     value_changed = True
            # print(event.direction, event.action)


if __name__ == "__main__":
    print("\nPython %s" % sys.version)
    print("IoT Hub Client for Python")

    iothub_client_sample_run(0.0)
    simulate_power_generation()
    # iothub_client_sample_run()
