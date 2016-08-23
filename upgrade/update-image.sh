#!/bin/sh
#
# Modify normal image to upgrade image
#

# Back rpm db up for Tizen 3.0
mkdir /system-update/data/rpm
cp -arf /var/lib/rpm/* /system-update/data/rpm

# remove RW partitions' files
rm -rf /opt/*
