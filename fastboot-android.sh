#!/bin/bash -x

adb() {
  command adb $@
}

fastboot() {
  until command fastboot -S 100M $@; do echo "Try again..."; sleep 2; done
}

adb reboot bootloader
fastboot devices

fastboot flash aboot emmc_appsboot.mbn
fastboot flash abootbak emmc_appsboot.mbn

fastboot flash boot boot.img

fastboot flash recovery recovery.img

fastboot -S 100M flash system system.img

fastboot flash vendor vendor.img

fastboot flash vbmeta vbmeta.img
fastboot flash vbmetabak vbmeta.img

fastboot flash product product.img

fastboot erase jvc

fastboot flash jvc jkc.img

fastboot flash dtbo dtbo.img
fastboot flash dtbobak dtbo.img

fastboot flash userdata userdata.img

fastboot flash splash splash.img
fastboot flash splash1 splash1.img

fastboot reboot

