#include <lazy_mount.h>
#include <stdio.h>
#include <stdlib.h>
#include <systemd/sd-daemon.h>
#include <string.h>

int get_input()
{
	int data;
	int i = 0;
	char c_data[2];
	while (1) {
	    data = getchar();
		if (i < 2)
			c_data[i] = (char)data;
		i++;
		if (data == 10 || data == 13)
			break;
	}
	if (i > 2)
		return -1;

	c_data[1] = 0;
	return atoi(c_data);
}

int main(int argc, char **argv)
{
	int data;
	int sl_ret;
	int i = 0;
	if (argc == 2 && strncmp(argv[1], "wait", 5) == 0) {
		for (i = 0 ; i < 3 ; i++) {
			sl_ret = wait_mount_user();
			if (sl_ret != 0) continue;
			else break;
		}

		if (i == 3) return -1;
		sd_notify(0, "READY=1");
		return 0;
	}
	while (1) {
		printf("Test\n");
		printf("1. get_need_ui_for_lazy_mount()\n");
		printf("2. do_mount_user()\n");
		printf("3. wait_mount_user()\n");
		printf("4. Exit to test.\n");
		printf("Select test : ");
		data = get_input();

		switch (data) {
		case 1:
			sl_ret = get_need_ui_for_lazy_mount();
		    printf("get_need_ui_for_lazy_mount() returns %d\n", sl_ret);
			break;
		case 2:
			printf("Doing mount user data....\n");
			sl_ret = do_mount_user();
		    printf("do_mount_user() returns %d\n", sl_ret);
			break;
		case 3:
			printf("Waiting mount user data....\n");
			sl_ret = wait_mount_user();
			printf("wait_mount_user() returns %d\n", sl_ret);
			break;
		case 4:
		    printf("exit\n");
			return 0;
		default:
		    printf("Unknown : %d\n", data);
			break;
		}
	}
	return 0;
}
