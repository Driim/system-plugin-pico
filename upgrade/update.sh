#!/bin/sh
#
# RW update script
#
PATH=/bin:/usr/bin:/sbin:/usr/sbin

PATCH_DIR=/usr/share/upgrade/scripts
RESULT_FILE=/upgrade_result
RUN=/bin/sh

# Change to normal mode from next booting
rm /system-update
rm /usr/lib/udev/rules.d/99-sdb-switch.rules

# Execute update scripts
if [ ! -d ${PATCH_DIR} ]
then
	echo "FAIL: Upgrade directory does not exist" > ${RESULT_FILE}
else
	PATCHES=`/bin/ls ${PATCH_DIR}`

	for PATCH in ${PATCHES}; do
		${RUN} ${PATCH_DIR}/${PATCH}
	done

	${RUN} /usr/share/upgrade/update-post.sh

	echo "SUCCESS: Upgrade successfully finished" > ${RESULT_FILE}
fi

# Reboot
reboot -f
