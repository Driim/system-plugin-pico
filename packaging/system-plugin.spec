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
Source3:   systemd-user-helper.manifest

Requires(post): /usr/bin/systemctl
Requires(post): /usr/bin/vconftool
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)

%description
This package provides target specific system configuration files.

%package u3
Summary:  U3/XU3 specific system configuration files
Requires: %{name} = %{version}-%{release}
Requires: %{name}-exynos = %{version}-%{release}
BuildArch: noarch

%description u3
This package provides U3/XU3 specific system configuration files.

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
License: Apache-2.0
Requires: vconf
Requires: liblazymount = %{version}

%description -n liblazymount
Library for lazy mount feature. It supports some interface functions.

%package -n liblazymount-devel
Summary: Development library for lazy mount feature
License:  Apache-2.0
Requires: vconf
Requires: liblazymount = %{version}

%description -n liblazymount-devel
Development library for lazy mount feature.It supports some interface functions.

%package -n systemd-user-helper
Summary: Systemd user launch helper for supporting Tizen specific feature
License: Apache-2.0

%description -n systemd-user-helper
Systemd user launch helper supports Tizen specific feature like directory compatibility and container.

%package -n system-upgrade
Summary: System upgrade available patch
License: Apache-2.0

%description -n system-upgrade
Systemd offline system update activation package

%prep
%setup -q

%build
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

./autogen.sh
%reconfigure \
		--disable-static \
		--prefix=%{_prefix} \
		--disable-debug-mode \
		--disable-eng-mode

%__make %{?jobs:-j%jobs}

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

ln -s ../tizen-system-env.service %{buildroot}%{_unitdir}/basic.target.wants/tizen-system-env.service

mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-exynos.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-spreadtrum.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

# umount /opt
install -m 644 units/umount-opt.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/local-fs-pre.target.wants
ln -s ../umount-opt.service %{buildroot}%{_unitdir}/local-fs-pre.target.wants/umount-opt.service

# fstab
mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab %{buildroot}%{_sysconfdir}
# ugly temporary patch for initrd wearable
install -m 644 etc/fstab_initrd %{buildroot}%{_sysconfdir}
# lazymnt
install -m 644 etc/fstab_lazymnt %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab_initrd_lazymnt %{buildroot}%{_sysconfdir}
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

# upgrade
mkdir -p %{buildroot}%{_datadir}
cp -r upgrade %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants
install -m 644 units/init-update.service %{buildroot}%{_unitdir}
install -m 644 units/offline-update.service %{buildroot}%{_unitdir}
ln -s ../init-update.service %{buildroot}%{_unitdir}/system-update.target.wants/init-update.service
ln -s %{_datadir}/upgrade %{buildroot}/system-update
install -m 644 rules/99-sdb-switch.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

%clean
rm -rf %{buildroot}

%post
systemctl daemon-reload

%post -n liblazymount
/sbin/ldconfig
/usr/bin/vconftool set -f -t int db/system/lazy_mount_show_ui 0
systemctl daemon-reload

%postun -n liblazymount  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/resize2fs@.service
%{_unitdir}/tizen-system-env.service
%{_unitdir}/basic.target.wants/tizen-system-env.service

%files u3
%manifest %{name}.manifest
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_sysconfdir}/fstab

%files n4
%manifest %{name}.manifest
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
%{_prefix}/lib/udev/rules.d/51-system-plugin-exynos.rules

%files circle
%manifest %{name}.manifest
/initrd
/csa
%{_sysconfdir}/fstab_initrd
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-system\x2ddata.service
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount
%{_unitdir}/umount-opt.service
%{_unitdir}/local-fs-pre.target.wants/umount-opt.service

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
/initrd
/csa
%{_prefix}/lib/udev/rules.d/51-system-plugin-spreadtrum.rules
%{_unitdir}/tizen-system-env.service
%{_sysconfdir}/fstab_initrd_lazymnt
%{_unitdir}/basic.target.wants/tizen-system-env.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-user.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dpartlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount
%{_unitdir}/umount-opt.service
%{_unitdir}/local-fs-pre.target.wants/umount-opt.service
%{_unitdir}/graphical.target.wants/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.service
%{_bindir}/tizen-fstrim-on-charge.sh

%files -n liblazymount
%defattr(-,root,root,-)
%{_libdir}/liblazymount.so.*
%manifest liblazymount.manifest
%{_unitdir}/basic.target.wants/lazy_mount.path
%{_unitdir}/lazy_mount.path
%{_unitdir}/lazy_mount.service
%{_bindir}/mount-user.sh
%if %{temp_wait_mount}
%{_bindir}/test_lazymount
%{_unitdir_user}/basic.target.wants/wait-user-mount.service
%{_unitdir_user}/wait-user-mount.service
%endif

%files -n liblazymount-devel
%defattr(-,root,root,-)
%manifest liblazymount.manifest
%{_libdir}/liblazymount.so
%{_includedir}/lazymount/lazy_mount.h
%{_libdir}/pkgconfig/liblazymount.pc
%if ! %{temp_wait_mount}
%{_bindir}/test_lazymount
%endif

%files -n system-upgrade
%{_datadir}/upgrade
%{_unitdir}/offline-update.service
%{_unitdir}/init-update.service
#%{_unitdir}/system-update.target.wants/offline-update.service
%{_unitdir}/system-update.target.wants/init-update.service
/system-update
%{_prefix}/lib/udev/rules.d/99-sdb-switch.rules

%files -n systemd-user-helper
%manifest systemd-user-helper.manifest
%caps(cap_sys_admin,cap_mac_admin,cap_mac_override,cap_dac_override,cap_setgid=ei) %{_bindir}/systemd_user_helper

%posttrans -n systemd-user-helper
cp -a /usr/lib/systemd/system/user\@.service /usr/lib/systemd/system/__user@.service
/usr/bin/sed -i -e 's/Type=\(.*\)/Type=simple/' /usr/lib/systemd/system/user\@.service
/usr/bin/sed -i -e 's/ExecStart=\(.*\)/ExecStart=\/usr\/bin\/systemd_user_helper %i/' /usr/lib/systemd/system/user\@.service
/usr/bin/sed -i -e '/RemainAfterExit=\(.*\)/d' /usr/lib/systemd/system/user\@.service
echo 'RemainAfterExit=yes' >> /usr/lib/systemd/system/user\@.service
