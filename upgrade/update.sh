#!/bin/sh
# RW update script
PATH=/bin:/usr/bin:/sbin:/usr/sbin

PATCH_DIR=/usr/share/upgrade/scripts
RESULT_FILE=/upgrade_result
RUN=/bin/sh

rm /system-update

if [ ! -d ${PATCH_DIR} ]
then
	echo "FAIL: Upgrade directory does not exist" > ${RESULT_FILE}
else
	PATCHES=`/bin/ls ${PATCH_DIR}`

	for PATCH in ${PATCHES}; do
		${RUN} ${PATCH_DIR}/${PATCH}
	done

	echo "SUCCESS: Upgrade successfully finished" > ${RESULT_FILE}
fi

systemctl reboot
