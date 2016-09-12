#!/bin/sh
#
# RW update script
#
PATH=/bin:/usr/bin:/sbin:/usr/sbin

PATCH_DIR=/usr/share/upgrade/scripts
UPDATE_DIR=/opt/upgrade
RESULT_FILE=${UPDATE_DIR}/update_result
UPDATE_LOG=${UPDATE_DIR}/update_log
RUN=/bin/sh

# Change to normal mode from next booting
rm /system-update

# Execute update scripts
if [ ! -d ${PATCH_DIR} ]
then
	echo "FAIL: Upgrade directory does not exist" > ${RESULT_FILE}
else
	mkdir -p ${UPDATE_DIR}

	echo "UPDATE: initializing" >> ${UPDATE_LOG}
	${RUN} /usr/share/upgrade/update-init.sh >> ${UPDATE_LOG} 2>&1

	PATCHES=`/bin/ls ${PATCH_DIR}`

	echo "UPDATE: RW update scripts" >> ${UPDATE_LOG}
	for PATCH in ${PATCHES}; do
		echo "${PATCH} is started..." >> ${UPDATE_LOG}
		${RUN} ${PATCH_DIR}/${PATCH} >> ${UPDATE_LOG} 2>&1
		echo "${PATCH} is ended..." >> ${UPDATE_LOG}
	done

	echo "UPDATE: post operations" >> ${UPDATE_LOG}
	${RUN} /usr/share/upgrade/update-post.sh >> ${UPDATE_LOG} 2>&1

	echo "SUCCESS: Upgrade successfully finished" >> ${RESULT_FILE}
fi

# Reboot
systemctl reboot
