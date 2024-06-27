import asyncio
from bleak import BleakScanner, BleakClient
import csv
import time
import datetime
import numpy as np

async def connect_to_ble_device(device_name, scan_time=10):
    scanner = BleakScanner()
    devices = await scanner.discover(timeout=scan_time)
    for device in devices:
        if device.name == device_name:
            client = BleakClient(device)
            await client.connect()
            return client
    return None

async def disconnect_from_ble_device(client):
    await client.disconnect()

async def get_characteristic(client, service_uuid, characteristic_uuid):
    for service in client.services:
        if service.uuid == service_uuid:
            characteristics = service.characteristics
            for characteristic in characteristics:
                if characteristic.uuid == characteristic_uuid:
                    return characteristic
    return None

def notification_handler(data_list):
    def handle(sender, data):
        timestamp = time.time()
        float_array = np.frombuffer(data, dtype='float32')
        data_list.append((timestamp, float_array))
    return handle

async def main(expreriment_id, duration):
    device_name = "InsoleDevice"

    controlService_uuid = "12345678-1234-1234-1234-1234567890ab"
    startStopCharacteristic_uuid = "12345678-1234-1234-1234-1234567890ad"

    dataService_uuid = "12345678-1234-1234-1234-1234567890ac"
    sensorDataCharacteristic_uuid = "12345678-1234-1234-1234-1234567890ae"
    derivedDataCharacteristic_uuid = "12345678-1234-1234-1234-1234567890af"

    dtime = datetime.datetime.now()
    filename = f"experiment_{expreriment_id}_" + dtime.strftime("%Y%m%d_%H%M%S") + ".csv"

    client = await connect_to_ble_device(device_name)
    if client is None:
        print("Device not found")
        return

    control_characteristic = await get_characteristic(client, controlService_uuid, startStopCharacteristic_uuid)
    await client.write_gatt_char(control_characteristic.uuid, (1).to_bytes(1, 'big'))

    data = []
    steps = []

    sensor_characteristic = await get_characteristic(client, dataService_uuid, sensorDataCharacteristic_uuid)
    await client.start_notify(sensor_characteristic, notification_handler(data))

    derived_characteristic = await get_characteristic(client, dataService_uuid, derivedDataCharacteristic_uuid)
    await client.start_notify(derived_characteristic, notification_handler(steps))

    await asyncio.sleep(duration)

    await client.write_gatt_char(control_characteristic.uuid, (0).to_bytes(1, 'big'))
    await client.stop_notify(sensor_characteristic)

    await disconnect_from_ble_device(client)

    # Save the data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Acceleration_X', 'Acceleration_Y', 'Acceleration_Z',
                      'Gyroscope_X', 'Gyroscope_Y', 'Gyroscope_Z',
                      'AnalogRead_0', 'AnalogRead_1', 'AnalogRead_2', 'AnalogRead_3',
                      'AnalogRead_4', 'AnalogRead_5', 'AnalogRead_6', 'AnalogRead_7']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            timestamp, values = entry
            writer.writerow({
                'Timestamp': timestamp,
                'Acceleration_X': values[0], 'Acceleration_Y': values[1], 'Acceleration_Z': values[2],
                'Gyroscope_X': values[3], 'Gyroscope_Y': values[4], 'Gyroscope_Z': values[5],
                'AnalogRead_0': values[6], 'AnalogRead_1': values[7], 'AnalogRead_2': values[8], 'AnalogRead_3': values[9],
                'AnalogRead_4': values[10], 'AnalogRead_5': values[11], 'AnalogRead_6': values[12], 'AnalogRead_7': values[13]
            })

    # save steps to a CSV file
    with open(f"steps_{filename}", 'w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Step']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in steps:
            timestamp, step = entry
            writer.writerow({
                'Timestamp': timestamp,
                'Step': step
            })

if __name__ == "__main__":
    print("Enter experiment id")
    exp_id = int(input())
    print("Enter experiment duration")
    duration = float(input())
    asyncio.run(main(exp_id, duration))
