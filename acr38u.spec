%define usbdropdir %(pkg-config libpcsclite --variable="usbdropdir" 2>/dev/null)
%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define build_version 100709

Summary:	ACS ACR 38 USB (acr38u) Smartcard Reader driver for PCSC-lite
Name:		acr38u
Version:	1.7.10
Release:	5
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.acs.com.hk/acr38_driversmanual.asp
Source0:	http://www.acs.com.hk/download/ACR38_LINUX_%{build_version}_P.tar.gz
Patch0:		acr38u-linkage_fix.diff
BuildRequires:	pkgconfig(libpcsclite)
Requires(post): pcsc-lite
Requires(postun): pcsc-lite
Requires:	pcsc-lite
Requires:	%{libname} = %{version}-%{release}

%description
CCID ACR38u Smart Card reader driver for PCSC-lite.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Shared library for %{name}

%description -n	%{libname}
Shared library for the CCID ACR38u Smart Card reader driver for
PCSC-lite.

%package -n	%{develname}
Summary:	Development library for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
Development files for the CCID ACR38u Smart Card reader driver for
PCSC-lite.

%prep
%setup -q -n ACR38_LINUX_%{build_version}_P
%patch0 -p0

%build
rm -rf autom4te.cache
autoreconf -fis

%configure2_5x \
	--disable-dependency-tracking \
	--disable-static \
	--enable-usbdropdir="%{buildroot}%{usbdropdir}"
%make

%install
%makeinstall_std

# move the .pc file to the correct place on x86-64
%ifarch x86_64
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_prefix}/lib/pkgconfig/libacr38ucontrol.pc %{buildroot}%{_libdir}/pkgconfig/libacr38ucontrol.pc
%endif

%post
/sbin/service pcscd condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service pcscd condrestart > /dev/null 2>/dev/null || :

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README* doc/README*
%{usbdropdir}

%files -n %{libname}
%defattr(-, root, root, 0755)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-, root, root, 0755)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.7.10-3mdv2011.0
+ Revision: 662752
- mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 1.7.10-2mdv2011.0
+ Revision: 603170
- rebuild

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 1.7.10-1mdv2010.1
+ Revision: 462618
- update to new version 1.7.10

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-8mdv2010.0
+ Revision: 413022
- rebuild

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 1.7.9-7mdv2009.1
+ Revision: 349983
- 2009.1 rebuild

* Wed Jul 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.7.9-6mdv2009.0
+ Revision: 230719
- added P0 to fix linkage
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.7.9-4mdv2008.1
+ Revision: 148420
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Jul 14 2007 Adam Williamson <awilliamson@mandriva.org> 1.7.9-3mdv2008.0
+ Revision: 51934
- correct major
- correct file list

* Sat Jul 14 2007 Adam Williamson <awilliamson@mandriva.org> 1.7.9-2mdv2008.0
+ Revision: 51925
- move .pc file to the correct place on x86-64
- er, restart pcscd not CUPS...
- take service restart commands from foomatic-db
- use mdv make and makeinstall macros
- quiet setup
- libify according to MDV policy
- correct buildrequires
- correct group
- initial spec from Cedric Devillers
- Import acr38u



* Thu Jul 12 2007 Cedric Devillers <brancaleone@altern.org> 1.7.9-1.mdv
- First mandriva build.
