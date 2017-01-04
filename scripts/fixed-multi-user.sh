#!/bin/sh
#
# Fixed Multi-User: executes fixed multiuser scripts
#
PATH=/bin:/usr/bin:/sbin:/usr/sbin

SCRIPT_DIR=/usr/share/fixed_multiuser/scripts

if [ ! -d ${SCRIPT_DIR} ]
then
	exit 0
fi

SCRIPTS=`/bin/ls ${SCRIPT_DIR}`

for SCRIPT in ${SCRIPTS}; do
	echo "Run ${SCRIPT}..."
	/bin/sh ${SCRIPT_DIR}/${SCRIPT}
done
