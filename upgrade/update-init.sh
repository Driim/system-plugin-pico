#!/bin/sh
#
# RW update initialize script
#
PATH=/bin:/usr/bin:/sbin:/usr/sbin
OWNER_HOME=/opt/usr/home/owner

# Create home directory
test ! -e /opt/usr/home && mkdir -p /opt/usr/home

if [ ! -d ${OWNER_HOME} ]
then
	gum-utils --offline --delete-user --uid=5001
	gum-utils --offline --add-user --username=owner --usertype=admin --usecret=tizen
fi
