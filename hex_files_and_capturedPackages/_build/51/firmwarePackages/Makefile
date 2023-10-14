ZIP_FILES := $(wildcard dfu_*.zip)
FOLDERS := $(patsubst %.zip, %, $(ZIP_FILES))


ifeq ($(fw1=app),true)
	file_dat := app
endif
ifeq ($(fw1=bl),true)
	file_dat := secure_bootloader
endif
ifeq ($(fw1=sd),true)
	file_dat := softdevice
endif

ifeq ($(fw2=app),true)
	file_dat := app
endif
ifeq ($(fw2=bl),true)
	file_dat := secure_bootloader
endif
ifeq ($(fw2=sd),true)
	file_dat := softdevice
endif

.PHONY: dump_all clean

dump_all: $(FOLDERS)

$(FOLDERS): %: %.zip
	unzip $< -d $@
	cd $@ && hexdump *.dat

clean:
	rm -rf dfu_bl

create1:
	unzip -o dfu_bl.zip -d dfu_bl
	hexdump dfu_bl/secure_bootloader.dat > output1.txt

create2:
	unzip -o dfu_bl.zip -d dfu_bl
	hexdump dfu_bl/secure_bootloader.dat > output2.txt

compare:
	@diff output1.txt output2.txt --side-by-side && echo "Same" || echo "Diffrent"
	


# diff <(hexdump dfu_app/app.dat| sed -n '5p') <(hexdump dfu_bl/secure_bootloader.dat| sed -n '5p') --side-by-side

# diff <(hexdump dfu_app/app.dat|head -n 5) <(hexdump dfu_bl/secure_bootloader.dat|head -n 5) --side-by-side
# diff <(hexdump dfu_app/app.dat|head -n 5) <(hexdump dfu_sd/softdevices.dat|head -n 5) --side-by-side

# diff <(rm -rf df_bl ; make firmware_bl; mkdir _build/51/firmwarePackages/dfu_bl; unzip _build/51/firmwarePackages/dfu_bl.zip -d _build/51/firmwarePackages/dfu_bl ;  hexdump _build/51/firmwarePackages/dfu_bl/secure_bootloader.dat) <(rm -rf dfu_bl ; make firmware_bl; unzip _build/51/firmwarePackages/dfu_bl.zip -d _build/51/firmwarePackages/dfu_bl ;  hexdump _build/51/firmwarePackages/dfu_bl/secure_bootloader.dat) --side-by-side
	
# diff <(rm -rf _build/51/firmwarePackages/dfu_bl ; make firmware_bl; mkdir _build/51/firmwarePackages/dfu_bl; unzip _build/51/firmwarePackages/dfu_bl.zip -d _build/51/firmwarePackages/dfu_bl ;  hexdump _build/51/firmwarePackages/dfu_bl/secure_bootloader.dat) <(rm -rf _build/51/firmwarePackages/dfu_bl ; make firmware_bl; mkdir _build/51/firmwarePackages/dfu_bl; unzip _build/51/firmwarePackages/dfu_bl.zip -d _build/51/firmwarePackages/dfu_bl ;  hexdump _build/51/firmwarePackages/dfu_bl/secure_bootloader.dat) --side-by-side