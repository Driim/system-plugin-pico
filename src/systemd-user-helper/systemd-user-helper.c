/*
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


#include <dlfcn.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <errno.h>
#include <limits.h>
#include <sys/stat.h>

#include <sched.h>
#include <sys/mount.h>

#include <tzplatform_config.h>

#define ARRAY_SIZE(name) (sizeof(name)/sizeof(name[0]))
#define PIDFILE_PATH ".systemd.pid"

// For compatibility, Using hard-coded path
#define LEGACY_CONTENTS_DIR "/opt/usr/media"
#define LEGACY_APPS_DIR "/opt/usr/apps"

#define LAZYMOUNT_LIB LIBDIR"/liblazymount.so.0"
#define CONTAINER_LIB LIBDIR"/security/pam_krate.so"

#define LOAD_SYMBOL(handle, sym, name) \
	do { \
		sym = dlsym(handle, name); \
		if (!sym) { \
			fprintf(stderr, "dlsym %s error\n", name); \
			dlclose(handle); \
			return -1; \
		} \
	} while (0);

static void *container_handle = NULL;

static const char *systemd_arg[] = {
	"/usr/lib/systemd/systemd",
	"--user",
	NULL
};

static int normal_user_preprocess(char *username)
{
	int r;
	r = unshare(CLONE_NEWNS);
	if (r < 0) {
		fprintf(stderr, "unshare failed\n");
		return r;
	}

	r = mount(NULL, "/", NULL, MS_SLAVE | MS_REC, NULL);
	if (r < 0) {
		fprintf(stderr, "Failed to change the propagation type of root to SLAVE\n");
		return r;
	}

	return 0;
}

static int normal_user_postprocess(char *username)
{
	int r;
	r = mount(tzplatform_getenv(TZ_USER_CONTENT),
			LEGACY_CONTENTS_DIR, NULL, MS_BIND, NULL);
	if (r < 0) {
		fprintf(stderr, "user content bind mount failed - %d\n", errno);
		return r;
	}

	r = mount(tzplatform_getenv(TZ_USER_APP),
			LEGACY_APPS_DIR, NULL, MS_BIND, NULL);
	if (r < 0) {
		fprintf(stderr, "user app bind mount failed - %d\n", errno);
		return r;
	}

	return 0;
}

static int container_open(void)
{
	if (container_handle)
		return 0;

	container_handle = dlopen(CONTAINER_LIB, RTLD_LAZY);
	if (!container_handle) {
		fprintf(stderr, "container module dlopen error\n");
		return -1;
	}
	return 0;
}

static int container_preprocess(char *username)
{
	int r;
	int (*handle_preprocess)(char *);

	r = container_open();
	if (r < 0)
		return r;

	LOAD_SYMBOL(container_handle, handle_preprocess, "container_preprocess");

	r = handle_preprocess(username);
	if (r < 0) {
		fprintf(stderr, "container module preprocess error\n");
		return r;
	}

	return 0;
}

static int container_postprocess(char *username)
{
	int r;
	int (*handle_postprocess)(char *);

	r = container_open();
	if (r < 0)
		return r;

	LOAD_SYMBOL(container_handle, handle_postprocess, "container_postprocess");

	r = handle_postprocess(username);
	if (r < 0) {
		fprintf(stderr, "container module postprocess error\n");
		return r;
	}

	return 0;
}

static int wait_condition(void)
{
	int r;
	void *h;

	int (*wait_mount_user)(void);

	r = access(LAZYMOUNT_LIB, F_OK);
	if (r < 0) {
		fprintf(stderr, "cannot find lazymount module - No support lazymount\n");
		return 0;
	}

	h = dlopen(LAZYMOUNT_LIB, RTLD_LAZY);
	if (!h) {
		fprintf(stderr, "lazymount module dlopen error\n");
		return -1;
	}

	LOAD_SYMBOL(h, wait_mount_user, "wait_mount_user");

	r = wait_mount_user();
	if (r < 0) {
		fprintf(stderr, "wait_mout_user failed\n");
		dlclose(h);
		return r;
	}

	dlclose(h);
	return 0;
}

static int make_pid_file(int pid, char* user_id)
{
	FILE *fp;
	char pidpath[PATH_MAX];
	int r = 0;

	snprintf(pidpath, PATH_MAX, "/run/user/%s/%s", user_id, PIDFILE_PATH);

	fp = fopen(pidpath, "w+");
	if (fp != NULL) {
		fprintf(fp, "%d", pid);
		fclose(fp);
	} else
		r = -1;

	return r;
}

int run_child(int argc, const char *argv[], char* user_id)
{
	pid_t pid;
	int r = 0;
	int i;

	if (!argv)
		return -EINVAL;

	pid = fork();

	if (pid < 0) {
		fprintf(stderr, "failed to fork");
		r = -errno;
	} else if (pid == 0) {
		for (i = 0; i < _NSIG; ++i)
			signal(i, SIG_DFL);

		r = execv(argv[0], (char **)argv);
		/* NOT REACH */
	} else{
		make_pid_file(pid, user_id);
		r = pid;
	}

	return r;
}

int main(int argc, char *argv[])
{
	int r = 0;
	int support_container = 0;

	if (argc < 2) {
		fprintf(stderr, "require user argument\n");
		return -1;
	}

	/* pre-processing */
	r = normal_user_preprocess(argv[1]);
	if (r < 0) {
		fprintf(stderr, "normal user preprocess failed\n");
		return r;
	}

	/* If container supports below funcs, below line should be enabled. */
	support_container = (access(CONTAINER_LIB, F_OK) == 0) ? 1 : 0;
	if (support_container) {
		r = container_preprocess(argv[1]);
		if (r < 0) {
			fprintf(stderr, "container preprocess failed\n");
			return r;
		}
	}

	r = run_child(ARRAY_SIZE(systemd_arg), systemd_arg, argv[1]);
	if (r < 0) {
		fprintf(stderr, "systemd user execution failed\n");
		return r;
	} else{
		fprintf(stderr, "success = pid = %d\n", r);
	}

	/* sync-style since there is no need to process other signal */
	wait_condition();

	/* post-processing */
	r = normal_user_postprocess(argv[1]);
	if (r < 0) {
		fprintf(stderr, "normal user postprocess failed\n");
		return r;
	}

	if (support_container) {
		r = container_postprocess(argv[1]);
		if (r < 0) {
			fprintf(stderr, "container postprocess failed\n");
			return r;
		}
	}

	return 0;
}


