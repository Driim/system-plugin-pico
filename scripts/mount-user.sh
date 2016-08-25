#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin

USER_DISK=`ls /dev/disk/by-partlabel/ | grep -i user`
USER_MNT=/opt/usr

if [ -f /tmp/.lazy_mount ]
then
rm -f /tmp/.lazy_mount
fi

if [ -f /run/.unlock_mnt ]
then
rm -f /run/.unlock_mnt
fi

mount | grep "$USER_MNT " > /dev/null

if [ $? = "0" ]
then
touch /run/.unlock_mnt
else
/usr/bin/mount PARTLABEL=$USER_DISK $USER_MNT
touch /run/.unlock_mnt
chsmack -a "_" $USER_MNT
fi
