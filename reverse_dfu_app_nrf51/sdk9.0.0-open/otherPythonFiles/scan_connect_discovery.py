from whad.ble import Scanner, Central, ConnectionEventTrigger, ReceptionTrigger, ManualTrigger
from whad.ble.profile import UUID
import whad.ble.connector

from whad.device import WhadDevice
from whad.exceptions import WhadDeviceNotFound

from scapy.all import BTLE_DATA, ATT_Hdr, L2CAP_Hdr, ATT_Read_Request, ATT_Write_Request, ATT_Error_Response, BTLE_EMPTY_PDU, BTLE_CTRL, LL_ENC_REQ

from time import time,sleep
import sys

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

def print_methods(obj):
    for method_name in dir(obj):
        print(method_name)

def show(packet):
    print(packet.metadata, repr(packet))

'''
Scan devices and select one
'''
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
