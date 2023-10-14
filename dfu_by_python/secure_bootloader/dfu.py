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
import sys, os, struct

import json # for using UUID database
import zipfile # for extracting the firmware zip file

# Path to the firmware zip file
if len(sys.argv) > 2:
    print("Error: Too many arguments.")
    print("Input path to of firmware zip file or leave it blank to use default path.")
    sys.exit(1)
elif len(sys.argv) == 2:
    firmware_zip_file_path = sys.argv[1]
else:
    firmware_zip_file_path = 'firmware_packages/dfu_app_blinky_nrf52832_s132_sdk17.1.0.zip'


# Extract firmware zip file to firmware_folder_path
def extract_zipfile(zipfile_path,zip_folder_path):
    with zipfile.ZipFile(zipfile_path, 'r') as file:
        file.extractall(zip_folder_path)

# Input firmware_folder_path
# Read manifest.json file inside this folder
# return type of firmware, path of dat_file and path of bin_file
def read_manifest(firmware_folder_path):
    manifest_file_path = firmware_folder_path +'/manifest.json'    
    
    with open(manifest_file_path, "r") as file:
        manifest_data = json.load(file)
    
        # manifest_data is a dict with key 'manifest'
        manifest_data = manifest_data['manifest']

    # extract type of firmware
    firmware_type = list(manifest_data.keys())[0]
    print("Firmware_type: %s" %firmware_type)
    
    # extract name of firmware dat_file
    firmware_dat_file_name = manifest_data[firmware_type]['dat_file']
    print("Firmware_dat_file_name: %s" %firmware_dat_file_name)
    firmware_dat_file_path = firmware_folder_path + '/' + firmware_dat_file_name

    # extract name of firmware bin_file
    firmware_bin_file_name = manifest_data[firmware_type]['bin_file']
    print("Firmware_bin_file_name: %s" %firmware_bin_file_name)
    firmware_bin_file_path = firmware_folder_path + '/' + firmware_bin_file_name

    return firmware_type, firmware_dat_file_path, firmware_bin_file_path

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


def get_size(file_path):
    size_file = os.path.getsize(file_path)  # Size of file in bytes
    sleep(1)
    size_file = struct.pack("<I", size_file)  # Convert to 4 bytes little endian
    return size_file


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
    

# Trigger DFU process - subscribe
def dfu_trigger(DFU_control_point):
    DFU_control_point.subscribe(
        notification = True,
        callback=on_charac_updated
    )
    sleep(3)
    print("---------")


# Select Command Object
def dfu_select_command_object(DFU_control_point):
    select = b"\x06"
    command_object = b"\x01"
    dfu_packet = select + command_object
    DFU_control_point.value = dfu_packet
    sleep(3)
    print("---------")


# Set PRN value (Packet Receipt Notification)
def dfu_set_PRN_value(PRN_value, DFU_control_point):
    PRN_code = b"\x02"

    dfu_packet = PRN_code + PRN_value
    DFU_control_point.value = dfu_packet
    sleep(3)
    print("---------")


# Create Command Object
def dfu_create_command_object(firmware_dat, DFU_control_point):
    create = b"\x01"
    command_object = b"\x01"
    size_object = get_size(firmware_dat)

    dfu_packet = create + command_object + size_object
    DFU_control_point.value = dfu_packet
    sleep(3)
    print("---------")

# Send Command Object
def dfu_send_command(firmware_dat, DFU_packet,mtu):
    with open(firmware_dat, "rb") as file:
        while True:
            # Read 20 bytes at a time from the file
            dfu_packet = file.read(mtu-3)
            
            # If there are no more bytes to read, break the loop
            if not dfu_packet:
                break
            
            print("dfu_packet: %s" % dfu_packet)
            # Send the packet
            DFU_packet.write(dfu_packet)
            sleep(0.04)
            print("---------")
    sleep(3)
    print("---------")
    

def dfu_send_packet(packet,DFU_packet):
    print("dfu_packet: %s" % packet)
    # Send the packet
    DFU_packet.write(packet)
    sleep(0.04)
    print("---------")
    
# Create Data Object
def dfu_create_data_object(size_object, DFU_control_point):
    print("Create Data Object\n")
    create = b"\x01"
    data_object = b"\x02"
    size_object = struct.pack("<I", size_object)  # Convert to 4 bytes little endian
    dfu_packet = create + data_object + size_object
    DFU_control_point.value = dfu_packet
    sleep(1)
    print("---------")

# Send firmware bin file which is a data object
def dfu_send_data_object(firmware_bin, DFU_packet, DFU_control_point, mtu):
    with open(firmware_bin, "rb") as file:
        file_size = os.path.getsize(firmware_bin)  # Size of file in bytes
        remain_size = file_size
    
        while True:
            # Create Data Object of 4096 bytes and send extractly 4096 bytes of data
            if remain_size >= 4096:
                # Create Data Object
                dfu_create_data_object(4096, DFU_control_point)
                read_data = 0 # Number of bytes read in this 4096 bytes of data
                # send file
                while True:
                    if read_data + (mtu-3) <= 4096:
                        packet = file.read(mtu-3)
                        dfu_send_packet(packet, DFU_packet)
                        read_data = read_data + (mtu-3)
                    else:
                        packet = file.read(4096-read_data)
                        dfu_send_packet(packet, DFU_packet)
                        break
                remain_size = remain_size - 4096
                
                # Request to calculate CRC and execute the sent file
                dfu_request_crc(DFU_control_point)
                dfu_execute_sent_file(DFU_control_point)
                
            # Create Data object and send the remaining data (which is < 4096 bytes)
            else:
                # Create Data Object
                dfu_create_data_object(remain_size, DFU_control_point)
                # send file
                while True:
                    packet = file.read(mtu-3)
                    if not packet:
                        break
                    dfu_send_packet(packet, DFU_packet)
                    
                # Request to calculate CRC and execute the sent file
                dfu_request_crc(DFU_control_point)
                dfu_execute_sent_file(DFU_control_point)
                
                # no more data to read
                break
            
        
# Request to calculate CRC
def dfu_request_crc(DFU_control_point):
    print("Request to calculate checksum \n")
    dfu_packet = b"\x03"
    DFU_control_point.value = dfu_packet
    sleep(3)
    print("---------")


# Execute the sent file (the dat file)
def dfu_execute_sent_file(DFU_control_point):
    print("Execute the sent file \n")
    dfu_packet = b"\x04"
    DFU_control_point.value = dfu_packet
    sleep(3)
    print("---------")


# Select last command and create Data Object
def dfu_select_last_command_and_create_data_object(DFU_control_point):
    select = b"\x06"
    data_object = b"\x02"

    dfu_packet = select + data_object
    DFU_control_point.value = dfu_packet
    sleep(3)
    print("---------")





# Scan devices and select one
print("Scanning devices...")

target_list = []

try:
    device = WhadDevice.create('hci0')
    scanner = Scanner(device)
    scanner.start()
    for i, result in enumerate(scanner.discover_devices()):
        print(f"{i}---{result}")
        target_list.append(result)

except (KeyboardInterrupt, SystemExit):
    scanner.stop()

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
print("\nSelected target:\n %s\n" % target)
target = target.address





central = Central(device)
print("Connecting to the target %s" % target)
device = central.connect(target, random=True)



# device = WhadDevice.create('hci0')
# central = Central(device)

# target = 'd4:37:ce:01:da:53'
# print("Connecting to the target %s" % target)
# device = central.connect(target, random=True)



sleep(1)
print("Connected to the target!\n")

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

c= device.get_characteristic(UUID("1800"), UUID("2aa6"))
print("value of characteristic Central Address Resolution")
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
    print("Target not support mtu = %s\n" %mtu)
    mtu = new_mtu


# Remove callback for mtu command
central.detach_callback(show_mtu)


# Get characteristics

DFU_packet = device.get_characteristic(
    UUID("FE59"),
    UUID("8ec90002-f315-4f60-9fb8-838830daea50"))
DFU_control_point = device.get_characteristic(
    UUID("FE59"),
    UUID("8ec90001-f315-4f60-9fb8-838830daea50"))


central.attach_callback(show)
# central.attach_callback(show_response_only)
sleep(1)
print("---------")


print("Extracting the firmware zip file\n")
firmware_folder_path = firmware_zip_file_path[:-4]
extract_zipfile(firmware_zip_file_path, firmware_folder_path)

print("Reading the manifest file\n")
firmware_type, firmware_dat, firmware_bin = read_manifest(firmware_folder_path)
sleep(1)

print("Trigger DFU process - Subscribe\n")
dfu_trigger(DFU_control_point)

print("Select Command Object\n")
dfu_select_command_object(DFU_control_point)

PRN_value = b"\x00\x00"
print("Set PRN value to %s\n" %PRN_value)
dfu_set_PRN_value(PRN_value, DFU_control_point)

print("Create Command Object\n")
dfu_create_command_object(firmware_dat, DFU_control_point)

print("Sending the firmware dat file\n")
dfu_send_command(firmware_dat, DFU_packet,mtu)

#Request to calculate checksum
dfu_request_crc(DFU_control_point)

#xecute the sent file - the firmware dat file
dfu_execute_sent_file(DFU_control_point)

PRN_value = b"\x0a\x00" # 10 packets will be sent before receiving a notification
print("Set PRN value to %s\n" %PRN_value)
dfu_set_PRN_value(PRN_value, DFU_control_point)

print("Select last command and create Data Object\n")
dfu_select_last_command_and_create_data_object(DFU_control_point)

# Already has crc request and execute command inside the function
print("Sending the firmware bin file\n")
dfu_send_data_object(firmware_bin, DFU_packet,DFU_control_point, mtu)




# Disconnect
print("Stop connection")
device.disconnect()
central.stop()
central.close()
