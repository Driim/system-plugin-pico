#!/bin/sh
#
# RW update post script
#
PATH=/bin:/usr/bin:/sbin:/usr/sbin

rm -rf /opt/usr/live
rm -rf /opt/driver
rm -rf /opt/storage

# Migrate user contents to 3.0 path
. /etc/tizen-platform.conf
export `tzplatform-get --user $TZ_SYS_DEFAULT_USER TZ_USER_CONTENT`
CONTENTS24=/opt/usr/media
CONTENTS30=$TZ_USER_CONTENT

cp -rT --preserve=mode,timestamps $CONTENTS24/DCIM      $CONTENTS30/Camera
cp -rT --preserve=mode,timestamps $CONTENTS24/Documents $CONTENTS30/Documents
cp -rT --preserve=mode,timestamps $CONTENTS24/Downloads $CONTENTS30/Downloads
cp -rT --preserve=mode,timestamps $CONTENTS24/Images    $CONTENTS30/Images
cp -rT --preserve=mode,timestamps $CONTENTS24/Music     $CONTENTS30/Music
cp -rT --preserve=mode,timestamps $CONTENTS24/Others    $CONTENTS30/Others
cp -rT --preserve=mode,timestamps $CONTENTS24/Sounds    $CONTENTS30/Sounds
cp -rT --preserve=mode,timestamps $CONTENTS24/Videos    $CONTENTS30/Videos

# Remove remain garbage files
rm -rf /opt/usr/media
mkdir -m 755 /opt/usr/media
chsmack -a '_' /opt/usr/media
rm -rf /opt/home/app
