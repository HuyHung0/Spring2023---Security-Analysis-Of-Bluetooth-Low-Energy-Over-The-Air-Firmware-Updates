from whad.ble import Central
from whad.ble.profile import CharacteristicDescriptor
from whad.device import WhadDevice

device = WhadDevice.create('hci0')
central = Central(device)
device = central.connect('ce:9b:3e:a0:0b:b5', random=True)

# Discover
device.discover()

for service in device.services():
    print(f'Service'+'-'*50)
    for charac in service.characteristics():
        if len(charac._Characteristic__descriptors) > 0:
            print("-----------This characteristic has descriptors: ")
            print("characteristic: %s", charac.handle)
            for descriptor in charac.descriptors():
                print(descriptor.value)
                print(descriptor.handle)
        else:
            print("-----------Descriptors.......: None")
        print("\n")
        
        
# Disconnect
print("Stop connection")
device.disconnect()
central.stop()
central.close()
