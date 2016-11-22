#!/bin/sh
#
# Modify normal image to upgrade image
#

# Back up rpm db for Tizen 3.0
mkdir /usr/share/upgrade/data/rpm
cp -af /var/lib/rpm/* /usr/share/upgrade/data/rpm

# Back up default user home directory
mkdir /usr/share/upgrade/data/home
cp -af /home/owner /usr/share/upgrade/data/home

# remove RW partitions' files
rm -rf /opt/*
