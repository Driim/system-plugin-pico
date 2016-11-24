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
chsmack -a "_" /opt/usr/home
cp -af /usr/share/upgrade/data/home/owner /opt/usr/home

# Copy 3.0 rpm db
rm -rf /var/lib/rpm/*
cp -af /usr/share/upgrade/data/rpm/* /var/lib/rpm


# For sdb debugging
/usr/share/upgrade/scripts/010.tizen-platform-config.patch.sh
/usr/share/upgrade/scripts/011.dlog_upgrade.sh
/usr/share/upgrade/scripts/011.security_upgrade.sh
/usr/share/upgrade/scripts/100.buxton2_upgrade.sh

# Prevent executing again
mv /usr/share/upgrade/scripts/010.tizen-platform-config.patch.sh /usr/share/upgrade
mv /usr/share/upgrade/scripts/011.dlog_upgrade.sh                /usr/share/upgrade
mv /usr/share/upgrade/scripts/011.security_upgrade.sh            /usr/share/upgrade
mv /usr/share/upgrade/scripts/100.buxton2_upgrade.sh             /usr/share/upgrade

####### filesystem update #######
rm -rf /var/lock
ln -snf /run/lock /var/lock

# Directory for compatibility
chown root:root /opt/usr/media
chsmack -a '_' -T /opt/usr/media
# The operation done by generic-base.post
chown root:root /opt/var/log
chsmack -a '*' -t /opt/var/log
