#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.68])
AC_INIT(liblazymount, 0.1, [BUG-REPORT-ADDRESS])

AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_HEADERS([config.h])

AC_USE_SYSTEM_EXTENSIONS
AC_SYS_LARGEFILE
AC_PREFIX_DEFAULT([/usr])
AM_INIT_AUTOMAKE([foreign])

LT_PREREQ(2.2)
LT_INIT([disable-static])

# Checks for programs.
AC_PROG_MKDIR_P
AC_PROG_LN_S
AC_PROG_SED
AC_PROG_GREP
AC_PROG_AWK
#AC_PROG_INSTALL

AC_PROG_CC
AM_PROG_CC_C_O
AC_PATH_PROG([M4], [m4])
M4_DEFINES=

# ------------------------------------------------------------------------------
our_cflags=" \
        -g -O2 \
        -Werror \
        -fpie"

our_ldflags=" \
        -Wl,--as-needed \
        -Wl,--no-undefined \
        -Wl,--gc-sections \
        -Wl,-z,relro \
        -Wl,-z,now \
        -pie"
#        -Wl,-fuse-ld=gold"

AC_SUBST([OUR_CFLAGS], "$our_cflags")
dnl AC_SUBST([OUR_CPPFLAGS], "$OUR_CFLAGS -Wp,-D_FORTIFY_SOURCE=2")
AC_SUBST([OUR_LDFLAGS], "$our_ldflags")

# ------------------------------------------------------------------------------
AC_ARG_WITH([rootprefix],
        AS_HELP_STRING([--with-rootprefix=DIR],
                [rootfs directory prefix for config files and kernel modules]),
                [], [with_rootprefix=${ac_default_prefix}])
AC_SUBST([rootprefix], [$with_rootprefix])

# ------------------------------------------------------------------------------
AC_ARG_WITH([rootlibdir],
        AS_HELP_STRING([--with-rootlibdir=DIR], [Root directory for libraries necessary for boot]),
        [],
        [with_rootlibdir=${libdir}])
AC_SUBST([rootlibdir], [$with_rootlibdir])

# ------------------------------------------------------------------------------
AC_ARG_ENABLE([debug-mode],
        AS_HELP_STRING([--disable-debug-mode], [disable debug mode]),
                [case "${enableval}" in
                        yes) enable_debug_mode=yes ;;
                        no) enable_debug_mode=no ;;
                        *) AC_MSG_ERROR(bad value ${enableval} for --disable-debug-mode) ;;
                esac],
                enable_debug_mode=yes)
if test "x$enable_debug_mode" == "xyes"; then
        M4_DEFINES="$M4_DEFINES -DDEBUG_MODE"
        AC_SUBST([OUR_CFLAGS], "$OUR_CFLAGS -DDEBUG_MODE -DTIZEN_DEBUG_ENABLE")
fi

AC_SUBST(DEBUG_MODE)
AM_CONDITIONAL([DEBUG_MODE], [test "x$enable_debug_mode" == "xyes"])

# ------------------------------------------------------------------------------
AC_ARG_ENABLE([eng-mode],
        AS_HELP_STRING([--disable-eng-mode], [disable engineer mode]),
                [case "${enableval}" in
                        yes) enable_eng_mode=yes ;;
                        no) enable_eng_mode=no ;;
                        *) AC_MSG_ERROR(bad value ${enableval} for --disable-eng-mode) ;;
                esac],
                enable_eng_mode=yes)
if test "x$enable_eng_mode" == "xyes"; then
        M4_DEFINES="$M4_DEFINES -DENG_MODE"
        AC_SUBST([OUR_CFLAGS], "$OUR_CFLAGS -DENG_MODE")
fi

AC_SUBST(ENG_MODE)
AM_CONDITIONAL([ENG_MODE], [test "x$enable_eng_mode" != "xno"])

# ------------------------------------------------------------------------------
AC_ARG_ENABLE([release-mode],
        AS_HELP_STRING([--enable-release-mode], [enable release mode]),
                [case "${enableval}" in
                        yes) enable_release_mode=yes ;;
                        no) enable_release_mode=no ;;
                        *) AC_MSG_ERROR(bad value ${enableval} for --enable-release-mode) ;;
                esac],
                enable_release_mode=no)
if test "x$enable_release_mode" == "xyes"; then
        M4_DEFINES="$M4_DEFINES -DRELEASE_MODE"
        AC_SUBST([OUR_CFLAGS], "$OUR_CFLAGS -DRELEASE_MODE")
fi

AC_SUBST(RELEASE_MODE)
AM_CONDITIONAL([RELEASE_MODE], [test "x$enable_release_mode" != "xno"])

# ------------------------------------------------------------------------------
AC_SUBST(M4_DEFINES)

# ------------------------------------------------------------------------------
PKG_CHECK_MODULES(VCONF, vconf)

# ------------------------------------------------------------------------------
AC_SUBST([LIBLAZYMOUNT_PC_REQUIRES], "")
AC_SUBST([LIBLAZYMOUNT_PC_CFLAGS], "-D_GNU_SOURCE -I${prefix}/include/lazymount")
AC_SUBST([LIBLAZYMOUNT_PC_LIBS], "-L${libdir} -llazymount")

AC_SUBST([LIBLAZYMOUNT_PC_REQUIRES], "${LIBLAZYMOUNT_PC_REQUIRES} ${VCONF_REQUIRES}")
AC_SUBST([LIBLAZYMOUNT_PC_CFLAGS], "${LIBLAZYMOUNT_PC_CFLAGS} ${VCONF_CFLAGS}")
AC_SUBST([LIBLAZYMOUNT_PC_LIBS], "${LIBLAZYMOUNT_PC_LIBS} ${VCONF_LIBS}")

# ------------------------------------------------------------------------------
AC_CONFIG_FILES([Makefile])

AC_OUTPUT
AC_MSG_RESULT([
        $PACKAGE_NAME $VERSION

        prefix:                  ${prefix}
        rootprefix:              ${with_rootprefix}
        sysconf dir:             ${sysconfdir}
        datarootdir:             ${datarootdir}
        lib dir:                 ${libdir}
        rootlib dir:             ${with_rootlibdir}
        debug mode:              ${enable_debug_mode}
        engineer mode:           ${enable_eng_mode}

        OUR CFLAGS:              ${OUR_CFLAGS} ${CFLAGS}
])
