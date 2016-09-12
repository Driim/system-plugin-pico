#!/bin/sh
#
# Modify normal image to upgrade image
#

# Back rpm db up for Tizen 3.0
mkdir /usr/share/upgrade/data/rpm
cp -arf /var/lib/rpm/* /usr/share/upgrade/data/rpm

# remove RW partitions' files
rm -rf /opt/*
