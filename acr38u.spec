%define usbdropdir %(pkg-config libpcsclite --variable="usbdropdir" 2>/dev/null)
%define release %mkrel 1
%define version	1.7.9
%define name	acr38u
%define	major	1	
#%define libname %mklibname %name %major
#%define libnamedev %mklibname %name %major -d
%define build_version 100709

Summary: ACS ACR 38 USB (acr38u) Smartcard Reader driver for PCSC-lite
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System Environment/Kernel
URL: http://www.acs.com.hk/acr38_driversmanual.asp
Packager: Cedric Devillers <cde@alunys.com>
Source: http://www.acs.com.hk/download/ACR38_LINUX_%{build_version}_P.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libpcsclite1-devel >= 1.3.1
Requires: pcsc-lite

%description
CCID ACR38u Smart Card reader driver for PCSC-lite.

#%package -n %{libnamedev}
#Summary: Header files, libraries and development documentation for %{name}.
#Group: Development/C
#Requires: %{libname} = %{version}
#
#%description -n %{libnamedev}
#This package contains the header files, development
#documentation for %{name}. If you like to develop programs using %{name},
#you will need to install %{libnamedev}.

%prep
%setup -n ACR38_LINUX_%{build_version}_P

%build
%configure \
	--disable-dependency-tracking \
	--disable-static \
	--enable-usbdropdir="%{buildroot}%{usbdropdir}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%post
/sbin/ldconfig
/sbin/service pcscd restart

%preun
/sbin/service pcscd restart

%postun
/sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README* doc/README*
%dir %{usbdropdir}/
%{usbdropdir}/ACR38UDriver.bundle/
%{_libdir}/libacr38ucontrol.so*
%{_prefix}/lib/pkgconfig/libacr38ucontrol.pc
%{_includedir}/ACS38DrvTools.h
%{_libdir}/libacr38ucontrol.la

#%files -n %{libnamedev}
#%defattr(-, root, root, 0755)
#%{_includedir}/ACS38DrvTools.h
#%{_libdir}/libacr38ucontrol.la
