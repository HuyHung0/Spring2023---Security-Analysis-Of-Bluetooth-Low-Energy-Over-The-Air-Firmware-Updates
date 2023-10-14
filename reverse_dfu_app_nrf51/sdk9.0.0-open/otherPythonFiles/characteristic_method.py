from whad.ble import Scanner, Central, ConnectionEventTrigger, ReceptionTrigger, ManualTrigger
from whad.ble.profile import UUID
import whad.ble.connector

from whad.device import WhadDevice
from whad.exceptions import WhadDeviceNotFound

from scapy.all import BTLE_DATA, ATT_Hdr, L2CAP_Hdr, ATT_Read_Request, ATT_Write_Request, ATT_Error_Response, BTLE_EMPTY_PDU, BTLE_CTRL, LL_ENC_REQ

from time import time,sleep
import sys


def print_methods(obj):
    for method_name in dir(obj):
        print(method_name)

def show(packet):
    print(packet.metadata, repr(packet))

device = WhadDevice.create('hci0')
central = Central(device)
device = central.connect('ce:9b:3e:a0:0b:b5', random=True)


# Discover
device.discover()

for service in device.services():
    print(f'Service'+'-'*50)
    print_methods(service)
    print('end service'+'-'*50)
    for charac in service.characteristics():
        print(f'Characteristic'+'-'*50)
        print(charac._Attribute__handle)
        print(charac.handle)
        print('---')
        print(charac._Attribute__uuid)
        print(charac.uuid)
        print_methods(charac)
        print("end characteristic"+'-'*50)
# Read Device Name characteristic (Generic Access Service)




# Disconnect
print("Stop connection")
device.disconnect()
central.stop()
central.close()
