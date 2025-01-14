#needsrootforbuild
Name:           ostree
Version:        2022.7
Release:        1
Summary:        A tool like git for operating system binaries
License:        LGPLv2+
URL:            https://ostree.readthedocs.io/en/latest/
Source0:        https://github.com/ostreedev/%{name}/releases/download/v%{version}/libostree-%{version}.tar.xz

Patch9000:      Do-not-run-testcase-test-libarvhive-import-because-selinux-is-off.patch
Patch9001:      skip-updating-the-preference.patch
Patch9002:      skip-if-etc-mtab-is-not-a-symlink-of-proc-self-mounts.patch

BuildRequires:  bison autoconf automake libtool gobject-introspection-devel pkgconfig(liblzma) docbook-xsl
BuildRequires:  pkgconfig(e2p) pkgconfig(zlib) pkgconfig(libcurl) pkgconfig(libsoup-2.4) gpgme-devel
BuildRequires:  pkgconfig(libselinux) pkgconfig(libcrypto) pkgconfig(fuse) pkgconfig(libsystemd)
BuildRequires:  dracut openssl-devel pkgconfig(mount) pkgconfig(libarchive) python3-pyyaml libxslt
BuildRequires:  gtk-doc elfutils-extra
Requires:       dracut systemd-units gnupg2
%ifarch x86_64
Requires: grub2
%else
Requires: grub2-efi
%endif

Provides:       ostree-libs ostree-grub2
Provides:       ostree-libs%{?_isa} = %{version}-%{release}
Obsoletes:      ostree-libs ostree-grub2

%description
This project is now known as "libostree", though it is still appropriate to use the previous name: "OSTree"
(or "ostree"). The focus is on projects which use libostree's shared library, rather than users directly
invoking the command line tools (except for build systems). However, in most of the rest of the documentation,
we will use the term "OSTree", since it's slightly shorter, and changing all documentation at once is impractical.

%package devel
Summary: Development headers for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package includes the header files for the %{name} library.

%package_help

%prep
%autosetup -n lib%{name}-%{version} -p1

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --with-selinux --with-curl --with-openssl --disable-silent-rules \
           --with-dracut=yesbutnoconf
%make_build

%install
%make_install
%delete_la

%check
make check

%post
%systemd_post ostree-remount.service
 
%preun
%systemd_preun ostree-remount.service

%files
%doc README.md
%license COPYING
%{_bindir}/%{name}
%{_bindir}/rofiles-fuse
%{_datadir}/%{name}
%{_datadir}/bash-completion/*/*
%{_prefix}/lib/dracut/modules.d/98ostree
%{_prefix}/lib/systemd/system-generators/*
%{_prefix}/lib/systemd/system/*
%{_prefix}/lib/tmpfiles.d/*
%{_prefix}/lib/%{name}
%{_libexecdir}/lib%{name}/*
%{_sysconfdir}/%{name}
%{_libdir}/*.so.1*
%{_libdir}/girepository-1.0/*
%{_sysconfdir}/grub.d/*
%{_libexecdir}/lib%{name}/grub2*
%exclude %{_libexecdir}/lib%{name}/*httpd

%files devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gir-1.0/*.gir

%files help
%{_mandir}/man*/{ostree,rofiles}*.gz

%changelog
* Sun Jan 29 2023 jiangchuangang <jiangchuangang@huawei.com> - 2022.7-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update to 2022.7
  add skip-if-etc-mtab-is-not-a-symlink-of-proc-self-mounts.patch for test failed

* Mon Oct 17 2022 yangmingtai <yangmingtai@huawei.com> - 2021.6-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add Buildrequires elfutils-extra

* Tue Feb 8 2022 yangzhuangzhuang <yangzhuangzhuang1@h-partners.com> - 2021.6-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update ostree to 2021.6

* Tue Jul 20 2021 wangchen <wangchen137@huawei.com> - 2020.8-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Delete unnecessary gdb from BuildRequires

* Fri Feb 5 2021 panxiaohe <panxiaohe@huawei.com> - 2020.8-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix failed tests about test-pull-summary-sigs.sh 

* Mon Jan 25 2021 zoulin <zoulin13@huawei.com> - 2020.8-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update ostree to 2020.8

* Wed Aug 12 2020 yangzhuangzhuang <yangzhuangzhuang1@huawei.com> - 2020.4-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:DO not run testcase test-libarchive-import,because selinux is off.

* Sat Jul 25 2020 linwei <linwei54@huawei.com> - 2020.4-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:update ostree to 2020.4

* Sat Mar 21 2020 openEuler Buildteam <buildteam@openeuler.org> - 2019.4-6
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add man files into help package

* Tue Feb 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 2019.4-5
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:enable check

* Sat Oct 19 2019 shenyangyang <shenyangyang4@huawei.com> - 2019.4-4
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add the version and release of ostree-libs%{?_isa}

* Fri Oct 18 2019 shenyangyang <shenyangyang4@huawei.com> - 2019.4-3
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add ostree-libs%{?_isa} that required by flatpak

* Mon Oct 14 2019 shenyangyang <shenyangyang4@huawei.com> - 2019.4-2
- Type: enhancement
- ID: NA
- SUG: NA
- DESC:delete unneeded build requires

* Mon Oct 14 2019 openEuler Buildteam <buildteam@openeuler.org> - 2019.4-1
- Package Init
