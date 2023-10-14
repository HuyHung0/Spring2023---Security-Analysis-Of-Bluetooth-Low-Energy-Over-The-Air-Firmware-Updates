# Before using this makefile, need to modify the version, sd_version, snr to compare
# with the board that we need to flash program (app, sd, bl,settings), create firmware packages.

# The erase and flashing the sniffer do not depend on the modification above.
version := 51

#--------------
# softdevice version of nrf52 s132 7.2.0
#sd_version := 0x101
#**************
# softdevice version of nrf51 s130 2.0.0
sd_version := 0x80

# board serial number
#-----------
#nrf51
snr := 681020882
#snr:=681578270
#***********
#nrf52
#snr := 682413350
#-----------

family := NRF$(version)
hw-version := $(version)


# bootloader
bl := sources/$(version)/bootloader.hex
# softdevices
sd := sources/$(version)/softdevices.hex
# application
app := sources/$(version)/app.hex

bl_sd_app := _build/$(version)/bl_sd_app.hex





# keys
key := keys/priv.pem

# dfu packages
dfu_bl := _build/$(version)/firmwarePackages/dfu_bl.zip
dfu_app := _build/$(version)/firmwarePackages/dfu_app.zip
dfu_sd := _build/$(version)/firmwarePackages/dfu_sd.zip

dfu_bl_sd := _build/$(version)/firmwarePackages/dfu_bl_sd.zip
dfu_sd_app := _build/$(version)/firmwarePackages/dfu_sd_app.zip
dfu_bl_sd_app := _build/$(version)/firmwarePackages/dfu_bl_sd_app.zip


#------------sniffer----------------
sniffer_51 := sources/51/sniffer.hex
sniffer_52 := sources/52/sniffer.hex

#------------create hex files----------------

# Create bootloader settings page
settings:
	@echo Creating: settings page
	@echo --- $(settings)
	@echo "\n"
	nrfutil settings generate --family $(family) --bootloader-version 1 --bl-settings-version 2 $(settings)
	@echo "\n"

# Merge bootloader and settings
merge_bl_settings: $(settings) $(bl)
	@echo Merging bootloader and settings page
	@echo "\n"
	mergehex --merge $(settings) $(bl) --output $(bl_settings)
	@echo "\n"


# Merge all files (settings, bootloader, softdevices, application)
merge_all52: $(settings) $(bl) $(sd) $(app)
	@echo Merging all: bootloader, settings, softdevices, application
	@echo --- $(settings)
	@echo --- $(bl)
	@echo --- $(sd)
	@echo --- $(app)
	@echo "\n"
	mergehex --merge $(settings) $(bl) $(sd) $(app) --output $(bl_settings_sd_app)
	@echo "\n"

# Merge all files (settings, bootloader, softdevices, application)
merge_bl_sd_app: $(bl) $(sd) $(app)
	@echo Merging all: bootloader, settings, softdevices, application
	@echo --- $(bl)
	@echo --- $(sd)
	@echo --- $(app)
	@echo "\n"
	mergehex --merge  $(bl) $(sd) $(app) --output $(bl_sd_app)
	@echo "\n"

# Flash the merged file
flash_merge_bl_sd_app: merge_bl_sd_app
	@echo Flashing: bootloader, softdevices, application
	@echo --- $(bl_sd_app)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(bl_sd_app) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"

# Flash the program
flash_app: $(app)
	@echo Flashing: application
	@echo --- $(app)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(app) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"

# Flash softdevice
flash_sd: $(sd)
	@echo Flashing: softdevices
	@echo --- $(sd)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(sd) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"

# Flash bootloader and softdevice and application
flash_bl_sd_app: $(sd) $(app) $(bl)
	@echo Flashing: bootloader, softdevices, application
	@echo --- $(sd)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(sd) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"
	@echo --- $(bl)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(bl) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"
	@echo --- $(app)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(app) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"



# Flash the bootloader
flash_bl: $(bl)
	@echo Flashing: secure bootloader
	@echo --- $(bl)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(bl) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"





# Flash the merge_all_files
flash_merge_all: merge_all
	@echo Flashing: the merged files of bootloader, settings, softdevices, application
	@echo Flashing: $(bl_settings_sd_app)
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --program $(bl_settings_sd_app) --sectorerase --verify
	@echo "\n"
	nrfjprog --family $(family) --snr $(snr) --reset
	@echo "\n"




# ---------------create dfu packages----------------

# Create firmware package: bootloader
firmware_bl: $(bl)
	@echo Creating firmware package: for bootloader package
	@echo --- $(bl)
	@echo "\n"
	nrfutil pkg generate --hw-version $(hw-version) --sd-req $(sd_version) --bootloader-version 1 --bootloader $(bl) --key-file $(key) $(dfu_bl)
	@echo "\n"

# Create firmware package: softdevices
firmware_sd: $(sd)
	@echo Creating firmware package: for softdevices package
	@echo --- $(sd)
	@echo "\n"
	nrfutil pkg generate --hw-version $(hw-version) --sd-req $(sd_version)  --softdevice $(sd) --key-file $(key) $(dfu_sd)
	@echo "\n"

# Create firmware package: app
firmware_app: $(app)
	@echo Creating firmware package: for application
	@echo --- $(app)
	@echo "\n"
	nrfutil pkg generate --hw-version $(hw-version) --sd-req $(sd_version) --application-version 1 --application $(app)  $(dfu_app)
	@echo "\n"

# Create firmware package: bl_sd
firmware_bl_sd: $(bl) $(sd)
	@echo Creating firmware package: for bootloader and softdevices
	@echo --- $(sd)
	@echo --- $(bl)
	@echo "\n"
	nrfutil pkg generate --hw-version $(hw-version) --sd-req $(sd_version) --sd-id $(sd_version) --softdevice $(sd) --bootloader-version 1 --bootloader $(bl) $(dfu_bl_sd)
	@echo "\n"

# Create firmware package: sd_app
firmware_sd_app: $(sd) $(app)
	@echo Creating firmware package: for softdevices and application
	@echo --- $(sd)
	@echo --- $(app)
	@echo "\n"
	nrfutil pkg generate --hw-version $(hw-version) --sd-req $(sd_version) --application $(app) --application-version 1 --sd-id $(sd_version) --softdevice $(sd) $(dfu_sd_app)
	@echo "\n"

# Create firmware package: bl_sd_app
firmware_bl_sd_app: $(bl) $(sd) $(app)
	@echo Creating firmware package: for bootloader, softdevices and application
	@echo --- $(bl)
	@echo --- $(sd)
	@echo --- $(app)
	@echo "\n"
	nrfutil pkg generate --hw-version $(hw-version) --sd-req $(sd_version) --application-version 1 --application $(app) --bootloader-version 1 --bootloader $(bl) --sd-id $(sd_version) --softdevice $(sd) $(dfu_bl_sd_app)
	@echo "\n"


# Create all packages
firmware_all: firmware_bl firmware_sd firmware_app firmware_bl_sd firmware_sd_app firmware_bl_sd_app
	@echo "\n"
	@echo "All packages created"
	@echo "\n"
# Clean files
clean:
	@echo Cleaning the firmware packages
	rm -rf $(dfu_bl) $(dfu_sd) $(dfu_app) $(dfu_bl_sd) $(dfu_sd_app) $(dfu_bl_sd_app)
	@echo "\n"




# Flash the sniffer
flash_sniffer_51: $(sniffer51)
	@echo Flashing: sniffer
	@echo --- $(sniffer51)
	@echo "\n"
	nrfjprog --family NRF51 --snr 681020882 --program $(sniffer_51) --sectorerase --verify
	@echo "\n"
	nrfjprog --family NRF51 --snr 681020882 --reset
	@echo "\n"


flash_sniffer_52: $(sniffer52)
	@echo Flashing: sniffer
	@echo --- $(sniffer52)
	@echo "\n"
	nrfjprog --family NRF52 --snr 682413350 --program $(sniffer_52) --sectorerase --verify
	@echo "\n"
	nrfjprog --family NRF52 --snr 682413350 --reset
	@echo "\n"


# Erase all in the board
erase52:
	nrfjprog --family NRF52 --snr 682413350 --eraseall


erase51:
	nrfjprog --family NRF51 --snr 681020882 --eraseall


# dump file
create_app1:
	make firmware_bl
	unzip -o $(dfu_app) -d _build/$(version)/firmwarePackages/dfu_app
	hexdump _build/$(version)/firmwarePackages/dfu_app/app.dat > dump_files/dump_app2.txt
create_bl2:
	make firmware_bl
	unzip -o $(dfu_bl) -d _build/$(version)/firmwarePackages/dfu_bl
	hexdump _build/$(version)/firmwarePackages/dfu_bl/secure_bootloader.dat > dump_b2.txt
compare:
	diff dump_bl.txt dump_b2.txt --side-by-side && echo "Files are identical" || echo "Files are different"



#------------check information----------------

fw-info:
	nrfutil device fw-info --serial-number $(snr)


