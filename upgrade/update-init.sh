#!/bin/sh
#
# RW update initialize script
#
PATH=/bin:/usr/bin:/sbin:/usr/sbin
OWNER_HOME=/opt/usr/home/owner

USER_DISK=`ls /dev/disk/by-partlabel/ | grep -i user`
USER_MNT=/opt/usr

# Mount user partition (specific to lazy mount)
mount | grep "$USER_MNT" > /dev/null

if [ $? != "0" ]
then
	/usr/bin/mount PARTLABEL=$USER_DISK $USER_MNT
fi

# Create home directory
test ! -e /opt/usr/home && mkdir -p /opt/usr/home

gum-utils --offline -u --uid 5001

# Copy 3.0 rpm db
rm -rf /var/lib/rpm/*
cp -arf /system-update/data/rpm/* /var/lib/rpm

# Disable cynara-check
buxton2ctl security-disable

####### filesystem update #######
rm -rf /var/lock
ln -snf /run/lock /var/lock

# Directory for compatibility
chown root:root /opt/usr/media
chsmack -a '_' -T /opt/usr/media
# The operation done by generic-base.post
chown root:root /opt/var/log
chsmack -a '*' -t /opt/var/log
