#!/bin/bash

PATH=/bin:/usr/bin:/sbin:/usr/sbin
interface=$1

/sbin/ifconfig ${interface} down
/sbin/ifconfig ${interface} 192.20.16.11
/sbin/ifconfig ${interface} up

