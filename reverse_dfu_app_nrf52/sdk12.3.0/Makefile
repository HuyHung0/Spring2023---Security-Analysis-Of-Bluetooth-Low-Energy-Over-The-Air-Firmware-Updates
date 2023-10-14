legacy_nrfutil = /home/studynewthing/apps/anaconda3/envs/py27/bin/nrfutil
nrfutil = /usr/bin/nrfutil

#nrf51 or nrf52
version := 52

#sd-req = 0x8c for s130 v3.0.0. List of code for sd-req is at the end of this file
sd-req = 0x8C



app := $(wildcard source/app*.hex)
bl := $(wildcard source/bl*.hex)
sd := $(wildcard source/sd*.hex)
key:= source/priv.pem

dfu_app := _build/dfu_app_hrs_s132_nrf52_sdk12.3.0.zip
dfu_sd := _build/dfu_sd_s132_nrf52_sdk12.3.0.zip
dfu_bl := _build/dfu_bl_s132_nrf52_sdk12.3.0.zip


flash_bl_sd_app:
	nrfjprog --eraseall
	@echo "\n"
	@echo Flash softdevices
	@echo "\n"
	nrfjprog --reset --program $(sd) --sectorerase --verify
	@echo "\n"
	@echo Flash bootloader
	@echo "\n"
	nrfjprog --reset --program $(bl) --sectorerase --verify
	@echo "\n"
	@echo Flash application
	@echo "\n"
	nrfjprog --reset --program $(app) --sectorerase --verify


firmware_app:
	$(nrfutil) pkg generate --hw-version $(version) --sd-req $(sd-req) --application-version 1 --application $(app) --key-file $(key) $(dfu_app)

firmware_sd:
	$(nrfutil) pkg generate --hw-version $(version) --sd-req $(sd-req) --softdevice $(sd) --key-file $(key) $(dfu_sd)

firmware_bl:
	$(nrfutil) pkg generate --hw-version $(version) --sd-req $(sd-req) --bootloader-version 1 --bootloader $(bl) --key-file $(key) $(dfu_bl)

erase:
	nrfjprog --eraseall

clean:
	rm -rf _build/*


# |s112_nrf52_6.0.0|0xA7|
# |s112_nrf52_6.1.0|0xB0|
# |s112_nrf52_6.1.1|0xB8|
# |s112_nrf52_7.0.0|0xC4|
# |s112_nrf52_7.0.1|0xCD|
# |s112_nrf52_7.2.0|0x103|
# |s112_nrf52_7.3.0|0x126|
# |s113_nrf52_7.0.0|0xC3|
# |s113_nrf52_7.0.1|0xCC|
# |s113_nrf52_7.2.0|0x102|
# |s113_nrf52_7.3.0|0x125|
# |s122_nrf52_8.0.0|0xEA|
# |s122_nrf52_8.1.1|0x112|
# |s130_nrf51_1.0.0|0x67|
# |s130_nrf51_2.0.0|0x80|
# |s130_nrf51_2.0.1|0x87|
# |s132_nrf52_2.0.0|0x81|
# |s132_nrf52_2.0.1|0x88|
# |s132_nrf52_3.0.0|0x8C|
# |s132_nrf52_3.1.0|0x91|
# |s132_nrf52_4.0.0|0x95|
# |s132_nrf52_4.0.2|0x98|
# |s132_nrf52_4.0.3|0x99|
# |s132_nrf52_4.0.4|0x9E|
# |s132_nrf52_4.0.5|0x9F|
# |s132_nrf52_5.0.0|0x9D|
# |s132_nrf52_5.1.0|0xA5|
# |s132_nrf52_6.0.0|0xA8|
# |s132_nrf52_6.1.0|0xAF|
# |s132_nrf52_6.1.1|0xB7|
# |s132_nrf52_7.0.0|0xC2|
# |s132_nrf52_7.0.1|0xCB|
# |s132_nrf52_7.2.0|0x101|
# |s132_nrf52_7.3.0|0x124|
# |s140_nrf52_6.0.0|0xA9|
# |s140_nrf52_6.1.0|0xAE|
# |s140_nrf52_6.1.1|0xB6|
# |s140_nrf52_7.0.0|0xC1|
# |s140_nrf52_7.0.1|0xCA|
# |s140_nrf52_7.2.0|0x100|
# |s140_nrf52_7.3.0|0x123|
# |s212_nrf52_6.1.1|0xBC|
# |s332_nrf52_6.1.1|0xBA|
# |s340_nrf52_6.1.1|0xB9|