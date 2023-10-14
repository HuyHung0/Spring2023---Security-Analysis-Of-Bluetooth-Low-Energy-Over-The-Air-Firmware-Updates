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

# Path to the firmware file
firmware = '_build/dfu_app_hrs_with_dfu_s132_nrf52_sdk11/app_hrs_with_dfu_s132_sdk11.0.0'
firmware_dat= firmware+'.dat'
firmware_bin= firmware+'.bin'

# Path to services and characteristics UUID database
characteristic_uuid_database_file ='../../bluetooth-numbers-database/v1/characteristic_uuids.json'
service_uuid_database_file ='../../bluetooth-numbers-database/v1/service_uuids.json'

# Import characteristic UUID database from 
# https://github.com/NordicSemiconductor/bluetooth-numbers-database/blob/master/v1/characteristic_uuids.json
with open(characteristic_uuid_database_file, "r") as f:
    characteristic_uuid_database = json.load(f)

# Import service UUID database from
# https://github.com/NordicSemiconductor/bluetooth-numbers-database/blob/master/v1/service_uuids.json
with open(service_uuid_database_file, "r") as f:
    service_uuid_database = json.load(f)


# Convert permission hex name
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


# Convert attribute type UUID to name
def attribute_type(uuid):
    if uuid == UUID('2800'):
        return "Primary Service"
    elif uuid==UUID("2801"):
        return "Secondary Service"
    elif uuid==UUID("2803"):
        return "Characteristic"
    else:
        return "Unknown"


# Search name of UUID in the database
def search_characteristic_uuid(uuid):
    for entry in characteristic_uuid_database:
        if entry["uuid"] == str(uuid).upper():
            return entry["name"]
    return "UUID not found."


# Search name of UUID in the database
def search_service_uuid(uuid):
    for entry in service_uuid_database:
            if entry["uuid"] == str(uuid).upper():
                return entry["name"]        
    return "UUID not found."


def print_methods(obj):
    for method_name in dir(obj):
        print(method_name)


# Show the packet
def show(packet):
    print(packet.metadata, repr(packet))
    print("\n")


# show the response packet only    
def show_response_only(packet):
    if packet.metadata.direction == 1:
        pass
    elif packet.metadata.direction == 2:
        print("Reply: %s " %repr(packet))
        print("\n")


# show and compute the mtu value of the response packet  
new_mtu = 0
def show_mtu(packet):
    global new_mtu
    print("Packet: %s" %packet.original)
    if len(packet.original) >= 7:
        new_mtu = packet.original[-2]    


def on_charac_updated(characteristic, value, indication=False):
    if indication:
        print('[indication] characteristic updated with value: %s' % value)
    else:
        print('[notification] characteristic updated with value: %s' % value)
    


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
sleep(1)
print("Connected to the target %s" % target.address)
'''


device = WhadDevice.create('hci0')
central = Central(device)

target_address = 'd4:37:ce:01:da:53'
print("Connecting to the target %s" % target_address)
device = central.connect(target_address, random=True)
sleep(2)
print("Connected to the target %s\n" % target_address)

sleep(1)
# Discover
print("Discovering services and characteristics....\n")
sleep(1)
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
        print(f"----------UUID......................: {charac.uuid}")
        print(f"----------Type......................: {charac.type_uuid}-{attribute_type(charac.type_uuid)}")
        print(f"----------Handle....................: {hex(charac.handle)}")
        print(f"----------Value Handle..............: {hex(charac.value_handle)}")
        print(f"----------Permissions...............: {hex(charac.properties)} : {convert_to_permissions(charac.properties)}")
        print(f"----------Name......................: {charac.name}")
        print(f"----------Name in database..........: {search_characteristic_uuid(charac.uuid)}")
        # Check if this characteristic has descriptor
        if len(charac._Characteristic__descriptors) > 0:
            print("----------Descriptors...............: Yes")
            for descriptor in charac.descriptors():
                print("----------------Descriptor handle...: %s" %hex(descriptor.handle))
                print("----------------Descriptor value....: %s" %descriptor.value)
        else:
            print("----------Descriptors...............: None")
        print("\n")



# Read popular characteristics
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


# Read specific characteristics: Legacy DFU Version
c = device.get_characteristic(UUID("00001530-1212-efde-1523-785feabcd123"), UUID("00001534-1212-efde-1523-785feabcd123"))
print("value of Legacy DFU Version")
print(c.value)
print("\n")

# callback for mtu command
central.attach_callback(show_mtu)

# Try a new mtu
# mtu= int(input("Set mtu which is not equal 23: "))
mtu = 50
print("Trying to set mtu = %s" %mtu)

device.set_mtu(mtu) #after this, the new_mtu will take value from the response packet
print("Mtu response is: %s" %new_mtu)
if new_mtu != mtu:
    print("Target not support mtu = %s" %mtu)
    mtu = new_mtu


# Remove callback for mtu command
central.detach_callback(show_mtu)


# Save some characteristics
legacyDFU_packet = device.get_characteristic(
    UUID("00001530-1212-efde-1523-785feabcd123"),
    UUID("00001532-1212-efde-1523-785feabcd123"))
legacyDFU_control_point = device.get_characteristic(
    UUID("00001530-1212-efde-1523-785feabcd123"),
    UUID("00001531-1212-efde-1523-785feabcd123"))


central.attach_callback(show)
# central.attach_callback(show_response_only)

# Subscribe to notification
print("Trigger DFU process - Subscribe\n")
legacyDFU_control_point.subscribe(
    notification = True,
    callback=on_charac_updated
)
sleep(3)
print("---------")

# Start DFU for application
print("Start DFU for application.\n")
startDFU = b'\x01'
app = b'\x04'

dfu_packet = startDFU + app
legacyDFU_control_point.value=dfu_packet
sleep(3)
print("---------")


# Write length of application
print("Write length of softdevice - bootloader - application\n")

len_softdevice = b'\x00\x00\x00\x00'
len_bootloader = b'\x00\x00\x00\x00'

# calculate app size:
app_size = os.path.getsize(firmware_bin)   
print("app_size: %s" %app_size)
len_application = struct.pack("<I", app_size)

dfu_packet = len_softdevice + len_bootloader + len_application
legacyDFU_packet.write(dfu_packet)
sleep(3)
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
with open(firmware_dat, "rb") as file:
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
with open(firmware_bin, "rb") as file:
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

# Disconnect
print("Stop connection")
device.disconnect()
central.stop()
central.close()
