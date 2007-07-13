%define usbdropdir %(pkg-config libpcsclite --variable="usbdropdir" 2>/dev/null)
%define release %mkrel 2
%define version	1.7.9
%define name	acr38u
%define	major	1	
%define libname %mklibname %name %major
%define develname %mklibname %name -d
%define build_version 100709

Summary: ACS ACR 38 USB (acr38u) Smartcard Reader driver for PCSC-lite
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: System/Kernel and hardware
URL: http://www.acs.com.hk/acr38_driversmanual.asp
Source: http://www.acs.com.hk/download/ACR38_LINUX_%{build_version}_P.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: pcsc-lite-devel >= 1.3.1
Requires(post): pcsc-lite
Requires(postun): pcsc-lite
Requires: pcsc-lite
Requires: %{libname} = %{version}-%{release}

%description
CCID ACR38u Smart Card reader driver for PCSC-lite.

%package -n %{libname}
Group: System/Libraries
Summary: Shared library for %{name}

%description -n %{libname}
Shared library for the CCID ACR38u Smart Card reader driver for
PCSC-lite.

%package -n %{develname}
Summary: Development library for %{name}
Group: Development/C
Requires: %{libname} = %{version}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files for the CCID ACR38u Smart Card reader driver for
PCSC-lite.

%prep
%setup -q -n ACR38_LINUX_%{build_version}_P

%build
%configure \
	--disable-dependency-tracking \
	--disable-static \
	--enable-usbdropdir="%{buildroot}%{usbdropdir}"
%make

%install
%{__rm} -rf %{buildroot}
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

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

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
%{_libdir}/*.*a
%{_libdir}/pkgconfig/*.pc
