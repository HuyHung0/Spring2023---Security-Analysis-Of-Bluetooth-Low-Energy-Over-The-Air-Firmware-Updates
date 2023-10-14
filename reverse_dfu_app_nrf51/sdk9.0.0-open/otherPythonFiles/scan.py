from whad.ble import Central, ConnectionEventTrigger, ReceptionTrigger, ManualTrigger
from whad.ble.profile import UUID
from whad.device import WhadDevice
from scapy.all import BTLE_DATA, ATT_Hdr, L2CAP_Hdr, ATT_Read_Request, ATT_Write_Request, ATT_Error_Response, BTLE_EMPTY_PDU, BTLE_CTRL, LL_ENC_REQ
from whad.ble import Scanner
from whad.exceptions import WhadDeviceNotFound
from time import time,sleep
import sys

def print_methods(obj):
    for method_name in dir(obj):
        print(method_name)

target_list = []

try:
    def show_packet(pkt):
        pkt.show()

    attack_device = WhadDevice.create('hci0')
    scanner = Scanner(attack_device)
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
print("Selected target:\n %s" % target_list[selected_number])

print("Stop connection")
device.disconnect()
central.stop()
central.close()
