%define lname	libacl

Name:           acl
BuildRequires:  libattr-devel
Summary:        Commands for Manipulating POSIX Access Control Lists
License:        GPL-2.0+ and LGPL-2.1+
Group:          Security/Access Control
Version:        2.2.51
Release:        0
Source:         %name-%version.src.tar.gz
Source2:        baselibs.conf
Source1001: 	acl.manifest
Url:            http://download.savannah.gnu.org/releases-noredirect/acl/

%description
getfacl and setfacl commands for retrieving and setting POSIX access
control lists.

%package -n %lname
Summary:        A dynamic library for accessing POSIX Access Control Lists
Group:          Security/Access Control

%description -n %lname
This package contains the libacl.so dynamic library which contains the
POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       %lname = %version
Requires:       glibc-devel
# the .so file references libattr.so.x, so require libattr-devel
Requires:       libattr-devel

%description -n libacl-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q -n acl-%version
cp %{SOURCE1001} .

%build
export OPTIMIZER="$RPM_OPT_FLAGS -fPIC"
export DEBUG=-DNDEBUG
CFLAGS="$RPM_OPT_FLAGS"
%configure \
	--prefix=/ \
	--exec-prefix=/ \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--enable-gettext=no \
	--disable-static \
	--with-pic
%{__make} %{?_smp_mflags}

%install
DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB
/usr/bin/make install DIST_MANIFEST="$DIST_INSTALL"
/usr/bin/make install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"
/usr/bin/make install-lib DIST_MANIFEST="$DIST_INSTALL_LIB"

rm -f %{buildroot}/%{_libdir}/*.{a,la}

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig


%docs_package

%files 
%manifest %{name}.manifest
%defattr(-,root,root)
%license doc/COPYING doc/COPYING.LGPL
%attr(755,root,root) %{_bindir}/chacl
%attr(755,root,root) %{_bindir}/getfacl
%attr(755,root,root) %{_bindir}/setfacl
%dir %attr(755,root,root) /usr/share/doc/packages/acl
%doc %attr(644,root,root) /usr/share/doc/packages/acl/CHANGES.gz
%doc %attr(644,root,root) /usr/share/doc/packages/acl/COPYING
%doc %attr(644,root,root) /usr/share/doc/packages/acl/COPYING.LGPL
%doc %attr(644,root,root) /usr/share/doc/packages/acl/PORTING
%doc %attr(644,root,root) /usr/share/doc/packages/acl/README

%files -n libacl-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%dir %attr(755,root,root) %{_includedir}/acl
%attr(644,root,root) %{_includedir}/acl/libacl.h
%attr(644,root,root) %{_includedir}/sys/acl.h
%attr(755,root,root) %{_libdir}/libacl.so

%files -n %lname
%manifest %{name}.manifest
%defattr(755,root,root,755)
%{_libdir}/libacl.so.1*

