legacy_nrfutil = /home/studynewthing/apps/anaconda3/envs/py27/bin/nrfutil
nrfutil = /usr/bin/nrfutil

app := $(wildcard app*.hex)
bl := $(wildcard bl*.hex)
sd := $(wildcard sd*.hex)
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
	nrfjprog --reset --family NRF52 --program sniffer.hex --sectorerase --verify

firmware_app:
	$(legacy_nrfutil) dfu genpkg --application-version 1 --application $(app) dfu_app_hrs_with_dfu_s130_nrf51_sdk11.zip

erase:
	nrfjprog --eraseall
