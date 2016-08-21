#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin

USER_DISK=`ls /dev/disk/by-partlabel/ | grep -i user`
USER_MNT=/opt/usr

mount | grep "/opt/usr"

if [ $? = "0" ]
then
touch /run/.unlock_mnt
else
/usr/bin/mount PARTLABEL=$USER_DISK $USER_MNT
touch /run/.unlock_mnt
fi
