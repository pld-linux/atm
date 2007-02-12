# $Revision: 1.42 $ $Date: 2007-02-12 00:48:39 $
Summary:	ATM on Linux
Summary(pl.UTF-8):   Obsługa sieci ATM w Linuksie
Name:		atm
Version:	0.78
Release:	1
License:	GPL
Group:		Networking
Source0:	ftp://lrcftp.epfl.ch/pub/linux/atm/dist/%{name}-%{version}.tar.gz
# Source0-md5:	64952e4d56285c0aeb12597d27884aff
Source1:	%{name}-pldrc.tar.gz
# Source1-md5:	c69820b03d8241e4cab33fef681df222
Patch0:		%{name}-opt.patch
Patch1:		%{name}-OPEN_MAX.patch
URL:		http://ica1www.epfl.ch/linux-atm/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ATM (Asynchronous Transfer Mode) networking for Linux is still under
development now but it works quite stable now and will most probably
be included in 2.4.x series kernels. In PLD Linux it consists of some
patches for current kernel version containing drivers for a few
popular ATM cards (ex. Fore, Madge, IDT) and PVC and SVC support. It
also includes programs and scripts providing the most popular ATM
services, i.e. Classical IP (IP over ATM), LAN Emulation clients and
servers, Multiprotocol Over ATM (MPOA) and some other goodies.

%description -l pl.UTF-8
Obsługa sieci ATM (Asynchronous Transfer Mode) w Linuksie mimo iż jest
jeszcze w stadium alfa działa już bardzo stabilnie i
najprawdopodobniej zostanie włączona do jąder serii 2.4.x. W Linuksie
PLD składa się ona z łat (patches) do bieżącej wersji jądra
zawierających sterowniki do kilku popularnych kart (m.in. Fore, Madge,
IDT) i zapewniających zestawianie połączeń PVC i SVC oraz zestawu
programów i skryptów (ten pakiet) realizujących najpopularniejsze
usługi ATM, tj. Classical IP (IP over ATM), klientów i serwery LAN
Emulation (LANE), Multiprotocol Over ATM (MPOA) i inne rozmaitości.

%package devel
Summary:	ATM on Linux - developer's package
Summary(pl.UTF-8):   Obsługa sieci ATM w Linuksie - biblioteki i pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Libraries and header files needed for development ATM applications for
Linux.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do opracowywania aplikacji ATM
dla Linuksa.

%prep
%setup -q -n %{name} -b 1
%patch0 -p1
%patch1 -p1

%build
# Test it before removing!
# gcc 2.95.x with optimizations turned on miscompiles atm 0.62!!!
RPM_OPT_FLAGS=""
export RPM_OPT_FLAGS
%{__make} depend
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig/interfaces,sysconfig/network-scripts,rc.d/init.d} \
	$RPM_BUILD_ROOT{/var/log/atm,%{_sysconfdir}/atm}

%{__make} install \
	INSTROOT=$RPM_BUILD_ROOT \
	INSTPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTMAN=$RPM_BUILD_ROOT%{_mandir}

install config/common/hosts.atm $RPM_BUILD_ROOT%{_sysconfdir}
install config/common/e164_cc $RPM_BUILD_ROOT%{_sysconfdir}

install config/pld/atm/* $RPM_BUILD_ROOT%{_sysconfdir}/atm/
install config/pld/init.d/atm $RPM_BUILD_ROOT/etc/rc.d/init.d/
install config/pld/sysconfig/atm $RPM_BUILD_ROOT/etc/sysconfig/
install config/pld/network-scripts/{ifup-atm,ifup-lec,ifdown-lec} \
		$RPM_BUILD_ROOT/etc/sysconfig/network-scripts
install config/pld/interfaces/{ifcfg-atm0,ifcfg-lec0} \
		$RPM_BUILD_ROOT/etc/sysconfig/interfaces

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add atm
%service atm restart

%preun
if [ "$1" = "0" ]; then
	%service atm stop
	/sbin/chkconfig --del atm
fi

%files
%defattr(644,root,root,755)
%doc doc/usage.txt BUGS CREDITS CHANGES README config/pld/README.PLD
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/atm/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hosts.atm
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/interfaces/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/atm
%attr(755,root,root) /etc/sysconfig/network-scripts/*
%attr(754,root,root) /etc/rc.d/init.d/atm
%config %{_sysconfdir}/e164_cc
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(751,root,root) /var/log/atm
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/*
