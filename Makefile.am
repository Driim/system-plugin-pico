ACLOCAL_AMFLAGS = -I m4 ${ACLOCAL_FLAGS}

SUBDIRS = .

# legacy rc script dir
rcdir=$(sysconfdir)/rc.d

# Inherit from systemd
systemdsysconfdir=$(sysconfdir)/systemd
systemconfigunitdir=$(systemdsysconfdir)/system
userconfigunitdir=$(systemdsysconfdir)/user
systemdignoreunitdir=$(systemdsysconfdir)/default-extra-dependencies
systemunitdir=$(rootprefix)/lib/systemd/system
userunitdir=$(prefix)/lib/systemd/user
udevlibexecdir=$(rootprefix)/lib/udev
udevhomedir=$(udevlibexecdir)
udevrulesdir=$(udevlibexecdir)/rules.d
sysctldir=$(prefix)/lib/sysctl.d
tmpfilesdir=$(prefix)/lib/tmpfiles.d

# DBus
dbussystemservicedir=$(prefix)/share/dbus-1/system-services

pkgconfiglibdir=$(libdir)/pkgconfig

# And these are the special ones for /
rootprefix=@rootprefix@
rootbindir=$(rootprefix)/bin
rootlibexecdir=$(rootprefix)/lib/system

CLEANFILES =
EXTRA_DIST =

lib_LTLIBRARIES =
noinst_LTLIBRARIES =
noinst_DATA =
pkgconfiglib_DATA =

bin_SCRIPTS =
rc_SCRIPTS =
SCRIPT_IN_FILES =
sysconf_DATA =
sysctl_DATA =
systemdsysconf_DATA =
systemdignoreunit_DATA =
systemconfigunit_DATA =
systemunit_DATA =
udevrules_DATA =
tmpfiles_DATA =
dbussystemservice_DATA =

DEFAULT_CFLAGS = \
	$(OUR_CFLAGS)

DEFAULT_LDFLAGS = \
	$(OUR_LDFLAGS)

AM_CPPFLAGS = \
	-include $(top_builddir)/config.h \
	-I $(top_srcdir)/src \
	-I $(top_srcdir)/src/shared \
	$(DEFAULT_CFLAGS)

AM_CFLAGS = $(DEFAULT_CFLAGS)
AM_LDFLAGS = $(DEFAULT_LDFLAGS)

INSTALL_EXEC_HOOKS =
UNINSTALL_EXEC_HOOKS =

SHUTDOWN_TARGET_WANTS =
LOCAL_FS_TARGET_WANTS =
BASIC_TARGET_WANTS =
SYSINIT_TARGET_WANTS =
SOCKETS_TARGET_WANTS =
TIMERS_TARGET_WANTS =
TIZEN_INIT_TARGET_WANTS =
TIZEN_BOOT_TARGET_WANTS =
TIZEN_SYSTEM_TARGET_WANTS =
TIZEN_RUNTIME_TARGET_WANTS =
MULTI_USER_TARGET_WANTS =
GRAPHICAL_TARGET_WANTS =
DEFAULT_TARGET_WANTS =
SYSCONF_LOCAL_FS_TARGET_WANTS =

install-target-wants-hook:
	where=$(systemunitdir) && what="$(SHUTDOWN_TARGET_WANTS)" && wants=shutdown.target && $(add-wants)
	where=$(systemunitdir) && what="$(LOCAL_FS_TARGET_WANTS)" && wants=local-fs.target && $(add-wants)
	where=$(systemunitdir) && what="$(BASIC_TARGET_WANTS)" && wants=basic.target && $(add-wants)
	where=$(systemunitdir) && what="$(MULTI_USER_TARGET_WANTS)" && wants=multi-user.target && $(add-wants)
	where=$(systemunitdir) && what="$(SYSINIT_TARGET_WANTS)" && wants=sysinit.target && $(add-wants)
	where=$(systemunitdir) && what="$(SOCKETS_TARGET_WANTS)" && wants=sockets.target && $(add-wants)
	where=$(systemunitdir) && what="$(TIMERS_TARGET_WANTS)" && wants=timers.target && $(add-wants)
	where=$(systemunitdir) && what="$(SLICES_TARGET_WANTS)" && wants=slices.target && $(add-wants)
	where=$(systemunitdir) && what="$(TIZEN_INIT_TARGET_WANTS)" && wants=tizen-init.target && $(add-wants)
	where=$(systemunitdir) && what="$(TIZEN_BOOT_TARGET_WANTS)" && wants=tizen-boot.target && $(add-wants)
	where=$(systemunitdir) && what="$(TIZEN_SYSTEM_TARGET_WANTS)" && wants=tizen-system.target && $(add-wants)
	where=$(systemunitdir) && what="$(TIZEN_RUNTIME_TARGET_WANTS)" && wants=tizen-runtime.target && $(add-wants)
	where=$(systemunitdir) && what="$(TIZEN_RUNTIME_TARGET_WANTS)" && wants=tizen-runtime.target && $(add-wants)
	where=$(systemunitdir) && what="$(GRAPHICAL_TARGET_WANTS)" && wants=graphical.target && $(add-wants)
	where=$(systemunitdir) && what="$(DEFAULT_TARGET_WANTS)" && wants=default.target && $(add-wants)
	where=$(systemunitdir) && what="$(CHARGING_MODE_TARGET_WANTS)" && wants=charging-mode.target && $(add-wants)
	where=$(systemconfigunitdir) && what="$(SYSCONF_LOCAL_FS_TARGET_WANTS)" && wants=local-fs.target && $(add-wants)

define add-wants
[ -z "$$what" -o -z "$$where" ] || ( \
	dir=$(DESTDIR)$$where/$$wants.wants && \
	$(MKDIR_P) -m 0755 $$dir && \
	cd $$dir && \
	rm -f $$what && \
	for i in $$what; do $(LN_S) ../$$i . || exit $$? ; done )
endef

INSTALL_EXEC_HOOKS += \
	install-target-wants-hook

# ------------------------------------------------------------------------------
pkgconfiglib_DATA += \
	src/liblazymount/liblazymount.pc

EXTRA_DIST += \
	src/liblazymount/liblazymount.pc.in

CLEANFILES += \
	src/liblazymount/liblazymount.pc

liblazymount_pkgincludedir=$(includedir)/lazymount
liblazymount_pkginclude_HEADERS =

liblazymount_pkginclude_HEADERS += src/liblazymount/lazy_mount.h

lib_LTLIBRARIES += \
	liblazymount.la

liblazymount_la_SOURCES = \
	src/liblazymount/lazy_mount.h \
	src/liblazymount/lazy_mount_interface.c

liblazymount_la_CFLAGS = \
	$(AM_CFLAGS) \
	$(LIBLAZYMOUNT_PC_CFLAGS)

liblazymount_la_LIBADD = \
	-L$(prefix)/lib \
	-lvconf

noinst_liblazymount_la_SOURCES = \
	src/liblazymount/lazy_mount.h \
	src/liblazymount/lazy_mount_interface.c

# ------------------------------------------------------------------------------
bin_PROGRAMS = \
	test_lazymount \
	systemd_user_helper

test_lazymount_SOURCES = \
	src/liblazymount/test_lazymount.c

test_lazymount_CFLAGS = \
	$(AM_CFLAGS) \
	-I. -Isrc/liblazymount \
	$(LIBLAZYMOUNT_PC_CFLAGS)

test_lazymount_LDADD = \
	-lvconf \
	-lsystemd \
	liblazymount.la

systemunit_DATA += \
	units/lazy_mount.path \
	units/lazy_mount.service

BASIC_TARGET_WANTS += \
	lazy_mount.path

bin_SCRIPTS = \
	scripts/mount-user.sh

systemd_user_helper_SOURCES = \
	src/systemd-user-helper/systemd-user-helper.c

systemd_user_helper_CFLAGS = \
	$(AM_CFLAGS) \
	${TZPLATFORMCONF_CFLAGS}

systemd_user_helper_LDADD = \
	${TZPLATFORMCONF_LIBS} \
	-ldl

# ------------------------------------------------------------------------------
substitutions = \
       '|rootlibexecdir=$(rootlibexecdir)|' \
       '|rootbindir=$(rootbindir)|' \
       '|bindir=$(bindir)|' \
       '|SYSTEMCTL=$(rootbindir)/systemctl|' \
       '|SYSTEMD_NOTIFY=$(rootbindir)/systemd-notify|' \
       '|systemdsysconfdir=$(systemdsysconfdir)|' \
       '|SYSTEM_CONFIG_UNIT_PATH=$(systemdsysconfdir)/system|' \
       '|USER_CONFIG_UNIT_PATH=$(systemdsysconfdir)/user|' \
       '|pkgdatadir=$(pkgdatadir)|' \
       '|systemunitdir=$(systemunitdir)|' \
       '|userunitdir=$(userunitdir)|' \
       '|systempresetdir=$(systempresetdir)|' \
       '|userpresetdir=$(userpresetdir)|' \
       '|udevhwdbdir=$(udevhwdbdir)|' \
       '|udevrulesdir=$(udevrulesdir)|' \
       '|catalogdir=$(catalogdir)|' \
       '|tmpfilesdir=$(tmpfilesdir)|' \
       '|sysctldir=$(sysctldir)|' \
       '|PACKAGE_VERSION=$(PACKAGE_VERSION)|' \
       '|PACKAGE_NAME=$(PACKAGE_NAME)|' \
       '|PACKAGE_URL=$(PACKAGE_URL)|' \
       '|LIBLAZYMOUNT_PC_REQUIRES=$(LIBLAZYMOUNT_PC_REQUIRES)|' \
       '|LIBLAZYMOUNT_PC_CFLAGS=$(LIBLAZYMOUNT_PC_CFLAGS)|' \
       '|LIBLAZYMOUNT_PC_LIBS=$(LIBLAZYMOUNT_PC_LIBS)|' \
       '|RANDOM_SEED=$(localstatedir)/lib/random-seed|' \
       '|prefix=$(prefix)|' \
       '|exec_prefix=$(exec_prefix)|' \
       '|libdir=$(libdir)|' \
       '|includedir=$(includedir)|' \
       '|VERSION=$(VERSION)|' \
       '|rootprefix=$(rootprefix)|' \
       '|udevlibexecdir=$(udevlibexecdir)|' \
       '|SUSHELL=$(SUSHELL)|' \
       '|DEBUGTTY=$(DEBUGTTY)|' \
       '|KILL=$(KILL)|' \
       '|KMOD=$(KMOD)|' \
       '|MKDIR_P=$(MKDIR_P)|' \
       '|QUOTAON=$(QUOTAON)|' \
       '|QUOTACHECK=$(QUOTACHECK)|' \
       '|SYSTEM_SYSVINIT_PATH=$(sysvinitdir)|' \
       '|VARLOGDIR=$(varlogdir)|' \
       '|RC_LOCAL_SCRIPT_PATH_START=$(RC_LOCAL_SCRIPT_PATH_START)|' \
       '|RC_LOCAL_SCRIPT_PATH_STOP=$(RC_LOCAL_SCRIPT_PATH_STOP)|' \
       '|PYTHON=$(PYTHON)|' \
       '|PYTHON_BINARY=$(PYTHON_BINARY)|' \
       '|INITAILBOOT_DONE=$(INITAILBOOT_DONE)|' \
       '|INITIALIZE_DONE=$(INITIALIZE_DONE)|' \
       '|READAHEAD_DIR=$(READAHEAD_DIR)|' \
       '|DIRTY_WRITEBACK_CENTISECS=$(DIRTY_WRITEBACK_CENTISECS)|'

SED_PROCESS = \
	$(AM_V_GEN)$(MKDIR_P) $(dir $@) && \
	$(SED) $(subst '|,-e 's|@,$(subst =,\@|,$(subst |',|g',$(substitutions)))) \
		< $< > $@

units/%: units/%.in Makefile
	$(SED_PROCESS)

%.rules: %.rules.in Makefile
	$(SED_PROCESS)

%.sh: %.sh.in Makefile
	$(SED_PROCESS)
	$(AM_V_GEN)chmod +x $@

src/%: src/%.m4
	$(AM_V_at)$(MKDIR_P) $(dir $@)
	$(AM_V_M4)$(M4) -P $(M4_DEFINES) < $< > $@

%.pc: %.pc.in
	$(SED_PROCESS)

units/%: units/%.m4 Makefile
	$(AM_V_M4)$(MKDIR_P) $(dir $@)
	$(AM_V_M4)$(M4) -P $(M4_DEFINES) -DFOR_SYSTEM=1 < $< > $@

sysctl.d/%: sysctl.d/%.in Makefile
	$(SED_PROCESS)

conf/%: conf/%.in
	$(SED_PROCESS)

conf/%: conf/%.m4
	$(AM_V_at)$(MKDIR_P) $(dir $@)
	$(AM_V_M4)$(M4) -P $(M4_DEFINES) < $< > $@

scripts/%: scripts/%.in
	$(SED_PROCESS)

scripts/%: scripts/%.m4
	$(AM_V_at)$(MKDIR_P) $(dir $@)
	$(AM_V_M4)$(M4) -P $(M4_DEFINES) < $< > $@

install-exec-hook: $(INSTALL_EXEC_HOOKS)
