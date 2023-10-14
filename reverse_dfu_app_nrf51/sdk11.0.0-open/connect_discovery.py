from whad.ble import Scanner, Central, ConnectionEventTrigger, ReceptionTrigger, ManualTrigger
from whad.ble.profile import UUID
import whad.ble.connector

from whad.device import WhadDevice
from whad.exceptions import WhadDeviceNotFound

from scapy.compat import raw

from time import time,sleep


import json # for using UUID database

def convert_to_permissions(number):
    permissions = {
        0x01: "Broadcast",
        0x02: "Read",
        0x04: "Write Without Response",
        0x08: "Write",
        0x10: "Notify",
        0x20: "Indicate",
        0x40: "Authenticated Signed Writes",
        0x80: "Extended Properties"
    }
    result = []
    for permission in permissions:
        if number & permission:
            result.append(permissions[permission])
    return result


def attribute_type(uuid):
    if uuid == UUID('2800'):
        return "Primary Service"
    elif uuid==UUID("2801"):
        return "Secondary Service"
    elif uuid==UUID("2803"):
        return "Characteristic"
    else:
        return "Unknown"
    


def print_methods(obj):
    for method_name in dir(obj):
        print(method_name)

def show(packet):
    print(packet.metadata, repr(packet))

def show_response_only(packet):
    if packet.metadata.direction == 1:
        pass
    elif packet.metadata.direction == 2:
        print("Reply: %s " %repr(packet))
        print("\n")
    
    
    
    
    
new_mtu = 0
def show_mtu(packet):
    global new_mtu
    #print_methods(packet)
    #print('-----------------')
    #print(packet.metadata, repr(packet))
    # print('---')
    print("Packet: %s" %packet.original)
    if len(packet.original) >= 7:
        new_mtu = packet.original[-2]
    # print('---')
    # print(packet.payload)
    # print('---')
    # print(packet.fields)
    # print('---')  
    # print(packet.getfield_and_val)
    # print('-----------------')

def on_charac_updated(characteristic, value, indication=False):
    if indication:
        print('[indication] characteristic updated with value: %s' % value)
    else:
        print('[notification] characteristic updated with value: %s' % value)
    


# Import characteristic UUID database from 
# https://github.com/NordicSemiconductor/bluetooth-numbers-database/blob/master/v1/characteristic_uuids.json
with open('../../bluetooth-numbers-database/v1/characteristic_uuids.json', "r") as f:
    characteristic_uuid_database = json.load(f)

# Search name of UUID in the database
def search_characteristic_uuid(uuid):
    for entry in characteristic_uuid_database:
        if entry["uuid"] == str(uuid).upper():
            return entry["name"]
            
    return "UUID not found."

# Import service UUID database from
# https://github.com/NordicSemiconductor/bluetooth-numbers-database/blob/master/v1/service_uuids.json
with open('../../bluetooth-numbers-database/v1/service_uuids.json', "r") as f:
    service_uuid_database = json.load(f)
def search_service_uuid(uuid):
    for entry in service_uuid_database:
            if entry["uuid"] == str(uuid).upper():
                return entry["name"]        



# Connect to target
device = WhadDevice.create('hci0')
central = Central(device)
device = central.connect('ce:9b:3e:a0:0b:b5', random=True)

#central.attach_callback(show)


# Discover
device.discover()

for service in device.services():
    print(f'Service'+'-'*50)
    print(f"--Service UUID......: {service.uuid}")
    print(f"--Service type......: {service.type_uuid}--{attribute_type(service.type_uuid)}")
    print(f"--Service handle....: {hex(service.handle)}")
    print(f"--Name..............: {service.name}")
    print(f"--Name in database..: {search_service_uuid(service.uuid)}")
    print("\n")
    #print_methods(service)
    for charac in service.characteristics():
        print('------ Characteristic')
        print(f"-----------UUID..............: {charac.uuid}")
        print(f"-----------Type..............: {charac.type_uuid}-{attribute_type(charac.type_uuid)}")
        print(f"-----------Handle............: {hex(charac.handle)}")
        print(f"-----------Value Handle......: {hex(charac.value_handle)}")
        print(f"-----------Permissions.......: {hex(charac.properties)} : {convert_to_permissions(charac.properties)}")
        print(f"-----------Name..............: {charac.name}")
        print(f"-----------Name in database..: {search_characteristic_uuid(charac.uuid)}")
        # Check if this characteristic has descriptor
        if len(charac._Characteristic__descriptors) > 0:
            print("-----------This characteristic has descriptor")   
        else:
            print("-----------Descriptors.......: None")
        print("\n")


# Read characteristic
c = device.get_characteristic(UUID("1800"), UUID("2a00"))
print("value of characteristic Peripheral Preferred Connection Parameters")
print(c.value)
print("\n")

c = device.get_characteristic(UUID("1800"), UUID("2a01"))
print("value of characteristic Appearance")
print(c.value)
print("\n")

c = device.get_characteristic(UUID("1800"), UUID("2a04"))
print("value of characteristic Peripheral Preferred Connection Parameters")
print(c.value)
print("\n")

c = device.get_characteristic(
    UUID("00001530-1212-efde-1523-785feabcd123"),
    UUID("00001534-1212-efde-1523-785feabcd123"))
print("value of characteristic Legacy DFU Version")
print(c.value)
print("\n")


# Disconnect
print("Stop connection")
device.disconnect()
central.stop()
central.close()
