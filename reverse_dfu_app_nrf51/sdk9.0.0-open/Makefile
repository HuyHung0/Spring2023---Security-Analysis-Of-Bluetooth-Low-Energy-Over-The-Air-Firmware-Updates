legacy_nrfutil = /home/studynewthing/apps/anaconda3/envs/py27/bin/nrfutil
nrfutil = /usr/bin/nrfutil

#all:
#	nrfjprog --reset --program $(pr) --sectorerase --verify

flash_bl_sd_app:
	nrfjprog --eraseall
	@echo Flash softdevices
	@echo "\n"
	nrfjprog --reset --program sd_s110.hex --sectorerase --verify
	@echo "\n"
	@echo Flash bootloader
	@echo "\n"
	nrfjprog --reset --program bl_dual_bank_ble_s110_nrf51422_sdk9.0.0.hex --sectorerase --verify
	@echo "\n"
	@echo Flash application
	@echo "\n"
	nrfjprog --reset --program app_hrs_s110_nrf51_sdk9.0.0.hex --sectorerase --verify

flash_sniffer52:
	nrfjprog --eraseall
	nrfjprog --reset --family NRF52 --program sniffer.hex --sectorerase --verify

firmware_app:
	$(legacy_nrfutil) dfu genpkg --application-version 1 --application app_hrs_s110_nrf51_sdk9.0.0.hex dfu_app_hrs_s110_nrf51_sdk9.0.0.zip

erase:
	nrfjprog --eraseall
