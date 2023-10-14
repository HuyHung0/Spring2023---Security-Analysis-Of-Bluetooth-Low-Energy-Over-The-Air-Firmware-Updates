legacy_nrfutil = /home/studynewthing/apps/anaconda3/envs/py27/bin/nrfutil
nrfutil = /usr/bin/nrfutil

# nrf51 or nrf52
version := 52

#sd-req of s132 2.0.0
sd-req = 0x81

app := $(wildcard source/app*.hex)
bl := $(wildcard source/bl*.hex)
sd := $(wildcard source/sd*.hex)
key:= source/priv.pem

dfu_app := _build/dfu_app_hrs_with_dfu_s132_nrf52_sdk11.zip

help:
	@echo "make flash_bl_sd_app"
	@echo "make firmware_app"
	@echo "make erase"

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
#	$(nrfutil) pkg generate --hw-version $(version) --sd-req $(sd-req) --application-version 1 --application $(app) --key-file $(key) $(dfu_app)
	$(legacy_nrfutil) dfu genpkg --application $(app) $(dfu_app)
erase:
	nrfjprog --eraseall
