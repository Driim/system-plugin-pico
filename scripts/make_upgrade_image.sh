#!/bin/sh
#
# make_upgrade_image.sh
#
#  Convert Tizen 3.0 platform image to upgrade image (2.4 -> 3.0)

# For sdb debugging

sdb_debugging=0
sdb_rule='SUBSYSTEM=="switch", ATTR{name}=="usb_cable", ATTR{state}=="1", RUN+="/usr/bin/direct_set_debug.sh --sdb-set"\nSUBSYSTEM=="switch", ATTR{name}=="usb_cable", ATTR{state}=="0", RUN+="/usr/bin/direct_set_debug.sh --sdb-unset"'

# Back up /home/owner & rpm db
backup () {
	echo "Back up home & rpm db"

	local tmp_path=$1

	umount ${tmp_path}
	e2fsck -f rootfs.img
	resize2fs rootfs.img 1G
	mount rootfs.img ${tmp_path}

	mount system-data.img ${tmp_path}/opt
	mount user.img ${tmp_path}/opt/usr

	mkdir ${tmp_path}/usr/share/upgrade/data/home
	cp -af ${tmp_path}/opt/usr/home/owner ${tmp_path}/usr/share/upgrade/data/home

	mkdir ${tmp_path}/usr/share/upgrade/data/rpm
	cp -af ${tmp_path}/opt/var/lib/rpm/* ${tmp_path}/usr/share/upgrade/data/rpm

	sync

	umount -l ${tmp_path}/opt/usr
	umount -l ${tmp_path}/opt

	umount ${tmp_path}
	e2fsck -f rootfs.img
	resize2fs -M rootfs.img
	mount rootfs.img ${tmp_path}
}

if [ `id -u` -ne 0 ]
then
	echo "make_upgrade_image.sh should be executed as root"
	exit
fi

if [ ! $1 ]
then
	echo "usage: $0 [tizen-3.0-image(tar.gz)]"
	exit
fi

echo "Decompressing $1"
imgs=`tar zxvf $1`

tmp_root=`mktemp -d system.XXX`
echo "Mount rootfs.img"
mount rootfs.img ${tmp_root}

cwd=`pwd`
backup ${cwd}/${tmp_root}

echo "Make /system-update"
ln -s /usr/share/upgrade/ ${tmp_root}/system-update

# For sdb debugging
if [ ${sdb_debugging} -eq 1 ]
then
	echo "Install sdb rule file"
	rule_file="99-sdb-switch.rules"
	echo ${sdb_rule} > ${rule_file}
	install -m 644 ${rule_file} ${tmp_root}/usr/lib/udev/rules.d
	rm ${rule_file}
fi

sync
umount ${tmp_root}

upgrade_img=`echo $1 | sed -e 's/\.tar\.gz//'`-upgrade.tar.gz
echo "Compressing upgrade image ${upgrade_img}"
tar zcf ${upgrade_img} dzImage modules.img rootfs.img

echo "Remove dummies"
rm -rf ${imgs} ${tmp_root}

echo "Done"
