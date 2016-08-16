#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin

USER_DISK=`ls /dev/disk/by-partlabel/ | grep -i user`
USER_MNT=/opt/usr

/usr/bin/mount PARTLABEL=$USER_DISK $USER_MNT
