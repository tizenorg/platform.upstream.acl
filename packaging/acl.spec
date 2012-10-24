Name:           acl
%define lname	libacl
BuildRequires:  libattr-devel
Summary:        Commands for Manipulating POSIX Access Control Lists
License:        GPL-2.0+ ; LGPL-2.1+
Group:          System/Filesystems
Version:        2.2.51
Release:        0
Source:         %name-%version.src.tar.gz
Source2:        baselibs.conf
Url:            http://download.savannah.gnu.org/releases-noredirect/acl/

%description
getfacl and setfacl commands for retrieving and setting POSIX access
control lists.

%package -n %lname
Summary:        A dynamic library for accessing POSIX Access Control Lists
Group:          System/Libraries

%description -n %lname
This package contains the libacl.so dynamic library which contains the
POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/C and C++
Requires:       %lname = %version
Requires:       glibc-devel
# the .so file references libattr.so.x, so require libattr-devel
Requires:       libattr-devel

%description -n libacl-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q -n acl-%version

%build
export OPTIMIZER="$RPM_OPT_FLAGS -fPIC"
export DEBUG=-DNDEBUG
CFLAGS="$RPM_OPT_FLAGS"
%configure \
	--prefix=/ \
	--exec-prefix=/ \
	--sbindir=/bin \
	--libdir=/%{_lib} \
    	--libexecdir=/%{_lib} \
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
%{__mkdir_p} %{buildroot}%{_libdir}
%{__ln_s} -v /%{_lib}/$(readlink %{buildroot}/%{_lib}/lib%{name}.so) %{buildroot}%{_libdir}/lib%{name}.so
%{__rm} -v %{buildroot}/%{_lib}/lib%{name}.{la,so}

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig


%docs_package

%files 
%defattr(-,root,root)
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
%defattr(-,root,root)
%dir %attr(755,root,root) %{_includedir}/acl
%attr(644,root,root) %{_includedir}/acl/libacl.h
%attr(644,root,root) %{_includedir}/sys/acl.h
%attr(755,root,root) %{_libdir}/libacl.so

%files -n %lname
%defattr(755,root,root,755)
/%{_lib}/libacl.so.1*

