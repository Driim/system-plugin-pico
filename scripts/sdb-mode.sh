#!/bin/sh

PATH=/bin:/usr/bin:/sbin:/usr/sbin


case "$1" in
	"--on")
		echo 0 > /sys/class/usb_mode/usb0/enable
		echo 04e8 > /sys/class/usb_mode/usb0/idVendor
		echo 6860 > /sys/class/usb_mode/usb0/idProduct
		echo "sdb" > /sys/class/usb_mode/usb0/funcs_fconf
		echo 239 > /sys/class/usb_mode/usb0/bDeviceClass
		echo 2 > /sys/class/usb_mode/usb0/bDeviceSubClass
		echo 1 > /sys/class/usb_mode/usb0/bDeviceProtocol
		echo 1 > /sys/class/usb_mode/usb0/enable
		systemctl start sdbd.service
		;;

	"--off")
		systemctl stop sdbd.service
		echo 0 > /sys/class/usb_mode/usb0/enable
		;;

	*)
		echo "Wrong parameters. Please use option --help to check options "
		;;
esac
