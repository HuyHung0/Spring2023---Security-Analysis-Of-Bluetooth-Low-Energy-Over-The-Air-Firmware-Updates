from whad.ble import Scanner, Central, ConnectionEventTrigger, ReceptionTrigger, ManualTrigger
from whad.ble.profile import UUID, CharacteristicProperties,CharacteristicDescriptor
import whad.ble.connector

from whad.device import WhadDevice
from whad.exceptions import WhadDeviceNotFound
from whad.protocol.whad_pb2 import Message

from scapy.all import BTLE, BTLE_DATA,\
    L2CAP_Hdr,\
    ATT_Hdr,  ATT_Read_Request, ATT_Read_Response,\
    ATT_Write_Request, ATT_Write_Response,\
    ATT_Write_Command, ATT_Handle_Value_Notification, ATT_Handle_Value_Indication,\
    ATT_Error_Response, BTLE_EMPTY_PDU, BTLE_CTRL, LL_ENC_REQ
from scapy.compat import raw

from time import time,sleep
import sys,os, struct

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
    #print("[Direction = %s ] " % packet.metadata.direction, end="")
    # if ATT_Hdr in packet:
    #     print(repr(packet[ATT_Hdr]))
        
    #     if ATT_Write_Request in packet:
    #         print("Write request: %s" %packet[ATT_Write_Request].fields)
    #     elif ATT_Write_Response in packet:
    #         print("Write response: %s" %packet[ATT_Write_Response].fields)
    #     elif ATT_Read_Request in packet:
    #         print("Read request: %s" %packet[ATT_Read_Request].fields)
    #     elif ATT_Read_Response in packet:
    #         print("Read response: %s" %packet[ATT_Read_Response].fields)
    #     elif ATT_Write_Command in packet:
    #         print("Write command: %s" %packet[ATT_Write_Command].fields)
    #     elif ATT_Handle_Value_Notification in packet:
    #         print("Notification: %s" %packet[ATT_Handle_Value_Notification].fields)
    #     elif ATT_Handle_Value_Indication in packet:
    #         print("Indication: %s" %packet[ATT_Handle_Value_Indication].fields)
    #     elif ATT_Error_Response in packet:
    #         print("Error response: %s" %packet[ATT_Error_Response].fields)
    #     elif BTLE_EMPTY_PDU in packet:
    #         print("Empty PDU")
    #     else:
    #         print("Unknown ATT packet")
    #print("\n")
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

'''
# Scan devices and select one

target_list = []

try:
    def show_packet(pkt):
        pkt.show()

    device = WhadDevice.create('hci0')
    scanner = Scanner(device)
    scanner.start()
    for i, result in enumerate(scanner.discover_devices()):
        print(f"{i}---{result}")
        target_list.append(result)

except (KeyboardInterrupt, SystemExit):
    pass

except WhadDeviceNotFound:
    print('[e] Device not found')
    exit(1)

print("\nPlease select a number between 0 and %s" % (len(target_list)-1))
selected_number = input('Select the target:  ')

while not selected_number.isdigit() or int(selected_number) >= len(target_list):
    print("Invalid input")
    print("\nPlease select a number between 0 and %s" % (len(target_list)-1))
    selected_number = input('Select again the target:  ')

selected_number = int(selected_number)
target=target_list[selected_number]
print("Selected target:\n %s" % target)



central = Central(device)
#central.attach_callback(show)

print("Connecting to the target %s" % target.address)
#print('Using device: %s' % central.device.device_id)
device = central.connect(target.address, random=True)
'''


device = WhadDevice.create('hci0')
central = Central(device)
device = central.connect('ce:9b:3e:a0:0b:b5', random=True)


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

# Try a new mtu
central.attach_callback(show_mtu)
#mtu= int(input("Set mtu which is not equal 23: "))
mtu =50
device.set_mtu(mtu)
print("New mtu is: %s" %new_mtu)
if new_mtu != mtu:
    print("Target not support mtu = %s" %mtu)
    print("Target probably is nrf51\n")
    mtu = new_mtu
central.detach_callback(show_mtu)

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



# Get characteristics

legacyDFU_control_point = device.get_characteristic(
    UUID("00001530-1212-efde-1523-785feabcd123"),
    UUID("00001531-1212-efde-1523-785feabcd123"))
legacyDFU_packet = device.get_characteristic(
    UUID("00001530-1212-efde-1523-785feabcd123"),
    UUID("00001532-1212-efde-1523-785feabcd123"))


central.attach_callback(show)
# central.attach_callback(show_response_only)

# Subscribe to notification
print("Subscribe\n")
legacyDFU_control_point.subscribe(
    notification = True,
    callback=on_charac_updated
)
sleep(4)
print("---------")

# Trigger DFU process
print("Trigger DFU process\n")
startDFU = b"\x01"
app = b"\04"

dfu_packet = startDFU + app
#print("dfu_packet: %s\n" %dfu_packet)
legacyDFU_control_point.value=dfu_packet
sleep(4)
print("---------")

# Write length of softdevice, bootloader and application to DFU packet
print("Write length of softdevice, bootloader and application\n")
len_softdevice = b"\x00\x00\x00\x00"
len_bootloader = b"\x00\x00\x00\x00"
# app: 29276 bytes = 0x725c
#len_application = b"\x5c\x72\x00\x00"
app_size = os.path.getsize("dfu_app_hrs_s110_nrf51_sdk9.0.0/app_hrs_s110_nrf51_sdk9.0.0.bin")   
print("app_size: %s" %app_size)
len_application = struct.pack("<I", app_size)

dfu_packet = len_softdevice + len_bootloader + len_application
#print("dfu_packet: %s\n" %dfu_packet)
legacyDFU_packet.write(dfu_packet)
sleep(4)
print("---------")

# Initialize DFU parameters
print("Initialize DFU parameters\n")
initializeDFU = b"\x02"
initPacket = b"\x00"

dfu_packet = initializeDFU+initPacket
#print("dfu_packet: %s\n" %dfu_packet)
legacyDFU_control_point.value=dfu_packet
sleep(4)
print("---------")

# Send init packet
print("Send init packet\n")
with open("dfu_app_hrs_s110_nrf51_sdk9.0.0/app_hrs_s110_nrf51_sdk9.0.0.dat", "rb") as file:
    while True:
        # Read 20 bytes at a time from the file
        dfu_packet = file.read(mtu-3)
        # If there are no more bytes to read, break the loop
        if not dfu_packet:
            break
        
        print("dfu_packet: %s" % dfu_packet)
        # Send the packet
        legacyDFU_packet.write(dfu_packet)
        sleep(4)
        print("---------")



# Initialize DFU parameters complete
print("Initialize DFU parameters complete\n")
initializeDFU = b"\x02"
initPacket = b"\x01" # Init packet complete

dfu_packet = initializeDFU+initPacket
#print("dfu_packet: %s\n" %dfu_packet)
legacyDFU_control_point.value=dfu_packet
sleep(4)
print("---------")

# Set PRN value (Packet Receipt Notification)
print("Set PRN value\n")
PRN_code = b"\x08"
PRN_value = b"\x0a\x00" # every 10 packets will receive one notification

dfu_packet = PRN_code+PRN_value
#print("dfu_packet: %s\n" %dfu_packet)
legacyDFU_control_point.write(dfu_packet)
sleep(4)
print("---------")

# Receive firmware image
print("Prepare to send firmware image\n")
opcode = b"\x03"

dfu_packet = opcode
legacyDFU_control_point.value=dfu_packet
sleep(4)
print("---------")

# Send firmware image
print("Sending firmware image\n")
with open("dfu_app_hrs_s110_nrf51_sdk9.0.0/app_hrs_s110_nrf51_sdk9.0.0.bin", "rb") as file:
    while True:
        # Read 20 bytes at a time from the file
        dfu_packet = file.read(mtu-3)
        # If there are no more bytes to read, break the loop
        if not dfu_packet:
            break
        
        print("dfu_packet: %s" % dfu_packet)
        # Send the packet
        legacyDFU_packet.write(dfu_packet)
        sleep(0.04)
        print("---------")


# Validate firmware image
print("Validate firmware image\n")
opcode = b"\x04"

dfu_packet = opcode
legacyDFU_control_point.value=dfu_packet
sleep(4)
print("---------")

# Activate
print("Activate\n")
opcode = b"\x05"

dfu_packet = opcode
legacyDFU_control_point.value=dfu_packet
sleep(4)
print("---------")



















# # method of central
# print("\n")
# print("------------Methods of central-------------")
# print_methods(central)
# print("\n")
# # method of device = central.connect()
# print("\n")
# print("------------Methods of device--------------")
# print_methods(device)
# print("\n")

# Disconnect
print("Stop connection")
device.disconnect()
central.stop()
central.close()
