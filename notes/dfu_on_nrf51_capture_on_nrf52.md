This is process of doing the DFU on board 51, captured package on board 52

SDK 12.3.0

1. Modify the Makefile.posix in sdk12.3.0/component/toolchain/gcc

   ```text
   GNU_INSTALL_ROOT = /usr/
   GNU_VERSION = 10.3.1
   GNU_PREFIX = arm-none-eabi
   ```

2. Clone micro-ecc to sdk12.3.0/external/micro-ecc/micro-ecc
   Then go to each folder nrf51_armgcc, nrf52_armgcc,..., run `make`

Folder hexfiles:
Change makefile the version and snr 51 and corresponding serial number

Run

```zsh
make flash_sd
make flash_bl
make flash_app
make firmware_bl_sd_app
make flash_
```

## Install gcc-arm-none-eabi

Download from this link
[https://launchpad.net/gcc-arm-embedded/4.9/4.9-2015-q1-update](https://launchpad.net/gcc-arm-embedded/4.9/4.9-2015-q1-update) and extract the zip file.
Sugguest that the extracted folder is
'/home/studynewthing/apps/gcc-arm-none-eabi/gcc-arm-none-eabi-4_9-2015q1'

sdk9.0.0

Then modify the 'Makefile.posix'
The original content:

```text
GNU_INSTALL_ROOT := /home/studynewthing/apps/gcc-arm-none-eabi/gcc-arm-none-eabi-4_8-2014q1
GNU_VERSION := 4.8.3
GNU_PREFIX := arm-none-eabi
```

We modify the path

```text
GNU_INSTALL_ROOT := /usr/local/gcc-arm-none-eabi-4_8-2014q1
GNU_VERSION := 4.9.3
GNU_PREFIX := arm-none-eabi
```
