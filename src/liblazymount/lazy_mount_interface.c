/*-*- Mode: C; c-basic-offset: 8; indent-tabs-mode: nil -*-*/

/*
 * liblazymount
 *
 * Copyright (c) 2016 Samsung Electronics Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the License);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <poll.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/inotify.h>
#include <vconf.h>

#ifndef VCONFKEY_SYSTEM_LAZY_MOUNT_SHOW_UI
#define VCONFKEY_SYSTEM_LAZY_MOUNT_SHOW_UI "db/system/lazy_mount_show_ui"
#endif
#define DEFAULT_VALUE_LAZY_MOUNT_SHOW_UI 0

#define LAZY_MOUNT_FILE "/tmp/.lazy_mount"
#define LAZY_MOUNT_CHECK_DIR "/run"
#define UNLOCK_MNT_STR ".unlock_mnt"
#define LAZY_MOUNT_CHECK_FILE LAZY_MOUNT_CHECK_DIR "/" UNLOCK_MNT_STR

#define EVENT_NAME_MAX 256
#define EVENT_SIZE  (sizeof(struct inotify_event))
#define EVENT_BUF_LEN     (512 * (EVENT_SIZE + EVENT_NAME_MAX))

/* Enumerate list of FDs to poll */
enum {
	FD_POLL_INOTIFY = 0,
	FD_POLL_MAX
};

int get_need_ui_for_lazy_mount()
{
	int sl_result = 0;
	/* get touchkey light duration setting */
	if (vconf_get_int(VCONFKEY_SYSTEM_LAZY_MOUNT_SHOW_UI, &sl_result) < 0)
		return DEFAULT_VALUE_LAZY_MOUNT_SHOW_UI;

	if (sl_result != 1 && sl_result != 0)
		return DEFAULT_VALUE_LAZY_MOUNT_SHOW_UI;

	return sl_result;
}

int do_mount_user()
{
	FILE *f = NULL;

	f = fopen(LAZY_MOUNT_FILE, "w");
	if (!f)
		return -errno;

	fclose(f);
	return 0;
}

int wait_mount_user()
{
	int fd, wd;
	char buffer[EVENT_BUF_LEN];
	int length;
	struct pollfd fds[FD_POLL_MAX];
	int i;

	fd = access(LAZY_MOUNT_CHECK_FILE, F_OK);

	if (fd == 0)
		return 0;

	fd = inotify_init();

	if (fd < 0)
		return -errno;

	wd = inotify_add_watch(fd, LAZY_MOUNT_CHECK_DIR, IN_CREATE|IN_MODIFY|IN_ATTRIB);

	fds[FD_POLL_INOTIFY].fd = fd;
	fds[FD_POLL_INOTIFY].events = POLLIN;

	while (1) {
		if (poll(fds, FD_POLL_MAX, -1) < 0) {
			inotify_rm_watch(fd, wd);
			close(fd);
			return -errno;
		}

		if (fds[FD_POLL_INOTIFY].revents & POLLIN) {
			length = read(fds[FD_POLL_INOTIFY].fd, buffer, EVENT_BUF_LEN);

			if (length < 0) {
				inotify_rm_watch(fd, wd);
				close(fd);
				return -errno;
			}

			i = 0;
			while (i < length) {
				struct inotify_event *event = (struct inotify_event *) &buffer[i];
				if (event->len > 0 && event->len < EVENT_NAME_MAX) {
					if (event->mask & (IN_CREATE|IN_MODIFY|IN_ATTRIB)) {
						if (!(event->mask & IN_ISDIR)) {
							if (!strncmp(event->name, UNLOCK_MNT_STR, sizeof(UNLOCK_MNT_STR))) {
								inotify_rm_watch(fd, wd);
								close(fd);
								return 0;
							}
						}
					}
				}
				i += EVENT_SIZE + event->len;
			}
		}
	}

	inotify_rm_watch(fd, wd);
	close(fd);

	return -1;
}
