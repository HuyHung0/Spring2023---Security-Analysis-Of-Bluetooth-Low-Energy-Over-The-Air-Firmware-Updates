- [How to capture bluetooth packages from Android phone](#how-to-capture-bluetooth-packages-from-android-phone)
  - [Analyse on wireshark](#analyse-on-wireshark)
  - [Write script](#write-script)

# How to capture bluetooth packages from Android phone

This instruction follows by a video in youtube [https://www.youtube.com/watch?v=NIBmiPtCDdM&t=515s](https://www.youtube.com/watch?v=NIBmiPtCDdM&t=515s). There are some modifications to match with my phone, but the general ideas are the same.

1. Enable Developer mode: Tap 7 times on "build Version" on "About phone" or similar label.
2. Disable bluetooth
3. Go to Developer option, enalbe Bluetooth HCI snoop log
4. Enable Bluetooth
5. Send some bluetooth command
6. Create a bugger report: depend on the phone
   1. On realme: in the Developer option, enable "Bug report shortcut"
   2. tap CPU in "All specs" 4 times to save a bug report
7. Disable HCI log
8. Now go to the computer to download the bug
   1. Enable Wireles debugging on Phone
   2. Copy the Ip address & port on Phone Wireless debugging
   3. Donwload SDK Platform Tools (Android.com -> What's news) and extract the zip file and go to this folder
   4. ./adb pair address:port password  
   5. ./adb connect address:port
   6. ./adb devices to see the connected device
   7. ./adb bugreport (it will download to current folder)
   8. unzip file.zip
   9. go to FS/data/misc/bluetooth/logs and we find the file btsnoop_hci.log

## Analyse on wireshark

Filter with `btatt`
Find all the Write request using the filter: `btatt.opcode.method==0x12`.
Record each command send from Phone
Two number in the end are checksum
A usefull website: crccalc.com to calculate the checksum of a value, find the algorithm

## Write script

Use gatttool:

```zsh
sudo gatttool -I
primary
```

Check the UUID

Install some library:

```zsh
pip install asyncio bleak crccheck
```

Here is an example from internet

```python
import asyncio
from bleak import BleakClient
from crccheck.crc import Crc8Maxim  #this is checksum algorithm

address = "D8:71:4D:31:09:68"

async def main(address):
   async with BleakClient(address) as client:
      header = bytes.fromhex("f0d10501")
      command = bytes.fromhex("30")       #30: turn on; 00: turn off the light
      params = bytes.fromhex("380c01")
      crcinst = Crc8Maxim()
      crcinst.process(header)
      crcinst.process(command)
      crcinst.process(params)
      model_number = await client.write_gatt_char("0000fec7-0000-1000-8000-00805f9b34fb", header + command + params + crcinst.finalbytes())

asyncio.run(main(address))
```
