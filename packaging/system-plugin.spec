#%define _unpackaged_files_terminate_build 0
#%define debug_package %{nil}

%define temp_wait_mount 1

Name:      system-plugin
Summary:   Target specific system configuration files
Version:   0.1
Release:   1
Group: Base/Startup
License:   Apache-2.0
Source0:   %{name}-%{version}.tar.bz2
Source1:   %{name}.manifest
Source2:   liblazymount.manifest

Requires(post): /usr/bin/systemctl
Requires(post): /usr/bin/udevadm
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(libsystemd)

%description
This package provides target specific system configuration files.

%package u3
Summary:  U3/XU3 specific system configuration files
Requires: %{name} = %{version}-%{release}
Requires: %{name}-exynos = %{version}-%{release}
BuildArch: noarch

%description u3
This package provides U3/XU3 specific system configuration files.

%package rpi3
Summary:  RPi3 specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description rpi3
This package provides RPi3 specific system configuration files.

%package iot
Summary:  IoT specific system configuration files
Requires: %{name} = %{version}-%{release}
Requires: dbus
BuildArch: noarch

%description iot
This package provides IoT specific system configuration files.

%package n4
Summary:  Note4 specific system configuration files
Requires: %{name} = %{version}-%{release}
Requires: %{name}-exynos = %{version}-%{release}
BuildArch: noarch

%description n4
This package provides Note4 specific system configuration files.

%package exynos
Summary:  Exynos specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description exynos
This package provides Exynos specific system configuration files.

%package spreadtrum
Summary:  Spreadtrum specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description spreadtrum
This package provides Spreadtrum specific system configuration files.

%package circle
Summary:  Circle specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description circle
This package provides Circle specific system configuration files.

%package -n liblazymount
Summary: Library for lazy mount feature
Requires(post): /usr/bin/vconftool
Requires: vconf

%description -n liblazymount
Library for lazy mount feature. It supports some interface functions.

%package -n liblazymount-devel
Summary: Development library for lazy mount feature
Requires: vconf
Requires: liblazymount = %{version}

%description -n liblazymount-devel
Development library for lazy mount feature.It supports some interface functions.

%package profile_ivi
Summary: ivi specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description profile_ivi
This package provides ivi specific system configuration files.

%package init_wrapper
Summary: Support init.wrapper booting.
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description init_wrapper
This package provides init.wrapper and init symlink file for init wrapper booting.

%package headless
Summary: Support headless device.
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description headless
This package provides the functions for headless device.

###################################################################
###################### Newly-created RPMs #########################
###################################################################

%package device-artik530
Summary: Artik530
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-artik530
This package provides system configuration files for the artik530 device.

%package device-artik710
Summary: Artik710
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-artik710
This package provides system configuration files for the artik710 device.

%package device-rpi3
Summary: RPI3
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-rpi3
This package provides system configuration files for the RPI3 device.

%package profile-iot
Summary:  System configuration files for IoT profiles
Requires: %{name} = %{version}-%{release}
Requires: dbus
BuildArch: noarch

%description profile-iot
This package provides system configuration files for IoT profiles.

%package profile-iot-headless
Summary:  System configuration files for IoT headless profiles
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description profile-iot-headless
This package provides system configuration files for IoT headless profiles.

%package config-udev-sdbd
Summary: System configuration files to trigger sdb with udev rule
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-udev-sdbd
This package provides configuration files to trigger sdb with udev rule.

%package feature-liblazymount
Summary: Library for lazy mount feature
Requires(post): /usr/bin/vconftool
Requires: vconf

%description feature-liblazymount
Library for lazy mount feature. It supports some interface functions.

%package feature-liblazymount-devel
Summary: Development library for lazy mount feature
Requires: vconf
Requires: feature-liblazymount = %{version}

%description feature-liblazymount-devel
Development library for lazy mount feature.It supports some interface functions.

%prep
%setup -q

%build
cp %{SOURCE1} .
cp %{SOURCE2} .

./autogen.sh
%reconfigure \
		--disable-static \
		--prefix=%{_prefix} \
		--disable-debug-mode \
		--disable-eng-mode

%__make %{?jobs:-j%jobs} \
	CFLAGS+=-DLIBDIR=\\\"%{_libdir}\\\"

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/csa
mkdir -p %{buildroot}/initrd
install -m 644 units/resize2fs@.service %{buildroot}%{_unitdir}
install -m 644 units/tizen-system-env.service %{buildroot}%{_unitdir}

# csa mount
install -m 644 units/csa.mount %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
ln -s ../csa.mount %{buildroot}%{_unitdir}/local-fs.target.wants/csa.mount

# Resize partition for 3-parted target
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-system\\x2ddata.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-user.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-rootfs.service

ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dpartlabel-user.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dpartlabel-system\\x2ddata.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dpartlabel-rootfs.service

ln -s ../tizen-system-env.service %{buildroot}%{_unitdir}/basic.target.wants/tizen-system-env.service

mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-exynos.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-spreadtrum.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/99-usb-ethernet.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

mkdir -p %{buildroot}%{_prefix}/lib/udev/hwdb.d/
install -m 644 rules/60-evdev.hwdb %{buildroot}%{_prefix}/lib/udev/hwdb.d/

# fstab
mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab %{buildroot}%{_sysconfdir}
# ugly temporary patch for initrd wearable
install -m 644 etc/fstab_initrd %{buildroot}%{_sysconfdir}
# lazymnt
install -m 644 etc/fstab_lazymnt %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab_initrd_lazymnt %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab_2part %{buildroot}%{_sysconfdir}
%if %{temp_wait_mount}
mkdir -p %{buildroot}%{_unitdir_user}/basic.target.wants
install -m 644 units/wait-user-mount.service %{buildroot}%{_unitdir_user}
ln -s ../wait-user-mount.service %{buildroot}%{_unitdir_user}/basic.target.wants/wait-user-mount.service
%endif

# fstrim
mkdir -p %{buildroot}%{_unitdir}/graphical.target.wants
install -m 644 units/tizen-fstrim-user.timer %{buildroot}%{_unitdir}
ln -s ../tizen-fstrim-user.timer %{buildroot}%{_unitdir}/graphical.target.wants/tizen-fstrim-user.timer
install -m 644 units/tizen-fstrim-user.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_bindir}
install -m 755 scripts/tizen-fstrim-on-charge.sh %{buildroot}%{_bindir}

# ivi
install -m 755 scripts/usb_net_init.sh %{buildroot}%{_bindir}

# fixed-multi-user
install -m 775 -D scripts/fixed-multi-user.sh %{buildroot}%{_datadir}/fixed_multiuser/fixed-multi-user.sh

# init_wrapper
mkdir -p %{buildroot}%{_sbindir}
install -m 755 scripts/init.wrapper %{buildroot}%{_sbindir}

# headless
mkdir -p %{buildroot}%{_sbindir}
install -m 755 scripts/sdb-mode.sh %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/99-sdb-switch.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 755 scripts/headless_env.sh %{buildroot}%{_sysconfdir}/profile.d

# config-udev-sdbd
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/99-sdb-extcon.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

%clean
rm -rf %{buildroot}

%post
systemctl daemon-reload

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/resize2fs@.service
%{_unitdir}/tizen-system-env.service
%{_unitdir}/basic.target.wants/tizen-system-env.service

%files u3
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_sysconfdir}/fstab
%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb

%post u3
%{_prefix}/bin/udevadm hwdb --update

%files rpi3
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_sysconfdir}/fstab
%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb

%post rpi3
%{_prefix}/bin/udevadm hwdb --update

%files iot
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_sysconfdir}/fstab_2part
%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb

%post iot
%{_prefix}/bin/udevadm hwdb --update
rm %{_sysconfdir}/fstab
mv %{_sysconfdir}/fstab_2part %{_sysconfdir}/fstab

%posttrans iot
# platform/upstream/dbus
rm -f %{_bindir}/dbus-cleanup-sockets
rm -f %{_bindir}/dbus-run-session
rm -f %{_bindir}/dbus-test-tool
rm -f %{_bindir}/dbus-update-activation-environment
rm -f %{_bindir}/dbus-uuidgen
# platform/upstream/e2fsprogs
rm -f %{_sbindir}/e4crypt

%files n4
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_sysconfdir}/fstab_lazymnt
%{_unitdir}/graphical.target.wants/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.service
%{_bindir}/tizen-fstrim-on-charge.sh

%files exynos
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_prefix}/lib/udev/rules.d/51-system-plugin-exynos.rules

%files circle
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
/initrd
/csa
%{_sysconfdir}/fstab_initrd
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-rootfs.service
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount

# ugly temporary patch for initrd wearable
%post circle
rm %{_sysconfdir}/fstab
mv %{_sysconfdir}/fstab_initrd %{_sysconfdir}/fstab
# fstab for tm1
%post spreadtrum
rm %{_sysconfdir}/fstab
mv %{_sysconfdir}/fstab_initrd_lazymnt %{_sysconfdir}/fstab
%post n4
rm %{_sysconfdir}/fstab
mv %{_sysconfdir}/fstab_lazymnt %{_sysconfdir}/fstab

%files spreadtrum
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
/initrd
/csa
%{_prefix}/lib/udev/rules.d/51-system-plugin-spreadtrum.rules
%{_unitdir}/tizen-system-env.service
%{_sysconfdir}/fstab_initrd_lazymnt
%{_unitdir}/basic.target.wants/tizen-system-env.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-rootfs.service
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount
%{_unitdir}/graphical.target.wants/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.service
%{_bindir}/tizen-fstrim-on-charge.sh
%{_datadir}/fixed_multiuser/fixed-multi-user.sh

%files -n liblazymount
%defattr(-,root,root,-)
%{_libdir}/liblazymount.so.*
%manifest liblazymount.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/lazy_mount.path
%{_unitdir}/lazy_mount.path
%{_unitdir}/lazy_mount.service
%{_bindir}/mount-user.sh
%if %{temp_wait_mount}
%{_bindir}/test_lazymount
%{_unitdir_user}/basic.target.wants/wait-user-mount.service
%{_unitdir_user}/wait-user-mount.service
%endif

%post -n liblazymount
/sbin/ldconfig
systemctl daemon-reload

%files -n liblazymount-devel
%defattr(-,root,root,-)
%manifest liblazymount.manifest
%license LICENSE.Apache-2.0
%{_libdir}/liblazymount.so
%{_includedir}/lazymount/lazy_mount.h
%{_libdir}/pkgconfig/liblazymount.pc
%if ! %{temp_wait_mount}
%{_bindir}/test_lazymount
%endif

%postun -n liblazymount  -p /sbin/ldconfig

%files profile_ivi
%license LICENSE.Apache-2.0
%{_prefix}/lib/udev/rules.d/99-usb-ethernet.rules
%{_bindir}/usb_net_init.sh

%files init_wrapper
%license LICENSE.Apache-2.0
%{_sbindir}/init.wrapper

%posttrans init_wrapper
rm -f /sbin/init
ln -s /sbin/init.wrapper /sbin/init

%files headless
%license LICENSE.Apache-2.0
%{_bindir}/sdb-mode.sh
%{_prefix}/lib/udev/rules.d/99-sdb-switch.rules
%{_sysconfdir}/profile.d/headless_env.sh

###################################################################
###################### Newly-created RPMs #########################
###################################################################

%files device-artik530

%files device-artik710

%files device-rpi3
#%manifest %{name}.manifest
#%license LICENSE.Apache-2.0
#%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
#%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
#%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
#%{_sysconfdir}/fstab
#%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb

%post device-rpi3
#%{_prefix}/bin/udevadm hwdb --update

%files profile-iot
#%manifest %{name}.manifest
#%license LICENSE.Apache-2.0
#%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
#%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
#%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
#%{_sysconfdir}/fstab_2part
#%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb

%post profile-iot
#%{_prefix}/bin/udevadm hwdb --update
#rm %{_sysconfdir}/fstab
#mv %{_sysconfdir}/fstab_2part %{_sysconfdir}/fstab

%posttrans profile-iot
## platform/upstream/dbus
#rm -f %{_bindir}/dbus-cleanup-sockets
#rm -f %{_bindir}/dbus-run-session
#rm -f %{_bindir}/dbus-test-tool
#rm -f %{_bindir}/dbus-update-activation-environment
#rm -f %{_bindir}/dbus-uuidgen
## platform/upstream/e2fsprogs
#rm -f %{_sbindir}/e4crypt

%files profile-iot-headless
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_sysconfdir}/profile.d/headless_env.sh

%files config-udev-sdbd
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/sdb-mode.sh
%{_prefix}/lib/udev/rules.d/99-sdb-extcon.rules

%files feature-liblazymount
#%defattr(-,root,root,-)
#%{_libdir}/liblazymount.so.*
#%manifest liblazymount.manifest
#%license LICENSE.Apache-2.0
#%{_unitdir}/basic.target.wants/lazy_mount.path
#%{_unitdir}/lazy_mount.path
#%{_unitdir}/lazy_mount.service
#%{_bindir}/mount-user.sh
#%if %{temp_wait_mount}
#%{_bindir}/test_lazymount
#%{_unitdir_user}/basic.target.wants/wait-user-mount.service
#%{_unitdir_user}/wait-user-mount.service
#%endif

%post feature-liblazymount
#/sbin/ldconfig
#systemctl daemon-reload

%files feature-liblazymount-devel
#%defattr(-,root,root,-)
#%manifest liblazymount.manifest
#%license LICENSE.Apache-2.0
#%{_libdir}/liblazymount.so
#%{_includedir}/lazymount/lazy_mount.h
#%{_libdir}/pkgconfig/liblazymount.pc
#%if ! %{temp_wait_mount}
#%{_bindir}/test_lazymount
#%endif

%postun feature-liblazymount  -p /sbin/ldconfig
