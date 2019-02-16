%define usbdropdir %(pkg-config libpcsclite --variable="usbdropdir" 2>/dev/null)
%define build_version 100709
%define major	0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	ACS ACR 38 USB (acr38u) Smartcard Reader driver for PCSC-lite
Name:		acr38u
Version:	1.7.10
Release:	13
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://www.acs.com.hk/acr38_driversmanual.asp
Source0:	http://www.acs.com.hk/download/ACR38_LINUX_%{build_version}_P.tar.gz
Patch0:		acr38u-linkage_fix.diff

BuildRequires:	pkgconfig(libpcsclite)
Requires(post,postun):	pcsc-lite
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

%package -n	%{devname}
Summary:	Development library for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Development files for the CCID ACR38u Smart Card reader driver for
PCSC-lite.

%prep
%setup -qn ACR38_LINUX_%{build_version}_P
%patch0 -p0

%build
rm -rf autom4te.cache
autoreconf -fis

%configure \
	--disable-dependency-tracking \
	--disable-static \
	--enable-usbdropdir="%{buildroot}%{usbdropdir}"
%make

%install
%makeinstall_std

# move the .pc file to the correct place on 64-bit platforms
%if "%{_libdir}" != "%{_prefix}/lib"
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_prefix}/lib/pkgconfig/libacr38ucontrol.pc %{buildroot}%{_libdir}/pkgconfig/libacr38ucontrol.pc
%endif

%post
/sbin/service pcscd condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service pcscd condrestart > /dev/null 2>/dev/null || :

%files
%doc AUTHORS ChangeLog COPYING README 
#doc/README
%{usbdropdir}

%files -n %{libname}
%{_libdir}/libacr38ucontrol.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

