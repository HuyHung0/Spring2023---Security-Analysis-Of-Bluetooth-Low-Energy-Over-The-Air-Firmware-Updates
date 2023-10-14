legacy_nrfutil = /home/studynewthing/apps/anaconda3/envs/py27/bin/nrfutil
nrfutil = /usr/bin/nrfutil

app = app_hrs_with_dfu_sd110_nrf51_sdk10.0.0.hex
bl = bl_dual_bank_ble_s110_nrf51422_sdk10.0.0.hex
sd = s110_nrf51_8.0.0_softdevice.hex
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
	$(legacy_nrfutil) dfu genpkg --application-version 1 --application $(app) dfu_app_hrs_with_dfu_s110_nrf51_sdk10.0.0.zip

erase:
	nrfjprog --eraseall
