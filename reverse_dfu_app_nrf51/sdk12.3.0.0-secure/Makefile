legacy_nrfutil = /home/studynewthing/apps/anaconda3/envs/py27/bin/nrfutil
nrfutil = /usr/bin/nrfutil

#nrf51 or nrf52
version := 51

#sd-req = 0x87 for s130
sd-req = 0x87

app := $(wildcard source/app*.hex)
bl := $(wildcard source/bl*.hex)
sd := $(wildcard source/sd*.hex)
key:= source/priv.pem

dfu_app := _build/dfu_app_hrs_s130_nrf51_sdk12.3.0.zip
#all:
#	nrfjprog --reset --program $(pr) --sectorerase --verify

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

flash_sniffer52:
	nrfjprog --eraseall
	nrfjprog --reset --family NRF52 --program sniffer52.hex --sectorerase --verify

firmware_app:
	$(nrfutil) pkg generate --hw-version $(version) --sd-req $(sd-req) --application-version 1 --application $(app) --key-file $(key) $(dfu_app)

erase:
	nrfjprog --eraseall
clean:
	rm -rf _build/*