# $Revision: 1.13.2.12 $ $Date: 2001-06-05 19:02:32 $
Summary:	ATM on Linux
Summary(pl):	Obs³uga sieci ATM w Linuxie
Name:		atm
Version:	0.78
Release:	8
License:	GPL
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe
URL:		http://ica1www.epfl.ch/linux-atm/
Source0:	ftp://lrcftp.epfl.ch/pub/linux/atm/dist/%{name}-%{version}.tar.gz
Source1:	%{name}-0.78.4-PLDrc.tar.gz
Source2:	http://home.sch.bme.hu/~cell/br2684/dist/001212/pppbr-001212-br2684ctl.c
Patch0:		%{name}-opt.patch
Patch1:		%{name}-OPEN_MAX.patch
Patch2:		%{name}-syslog.patch
Patch3:		%{name}-shared.patch
Patch4:		%{name}-br2684ctl-syslog.patch
Icon:		atm-logo.gif
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

%description -l pl
Obs³uga sieci ATM (Asynchronous Transfer Mode) w Linuxie mimo i¿ jest
jeszcze w stadium alfa dzia³a ju¿ bardzo stabilnie i
najproawdopodobniej zostanie w³±czona do j±der serii 2.4.x. W Linuxie
PLD sk³ada siê ona z ³at (patches) do bie¿±cej wersji j±dra
zawieraj±cych sterowniki do kilku popularnych kart (m.in Fore, Madge,
IDT) i zapewniaj±cych zestawianie po³±czeñ PVC i SVC oraz zestawu
programów i skryptów (ten pakiet) realizuj±cych najpopularniejsze
us³ugi ATM, tj. Classical IP (IP over ATM), klientów i serwery LAN
Emulation (LANE), Multiprotocol Over ATM (MPOA) i inne rozmaito¶ci.

%package devel
Summary:	ATM on Linux - developer's package
Summary(pl):	Obs³uga sieci ATM w Linuxie - biblioteki i pliki nag³ówkowe
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Libraries and header files needed for development ATM applications for
Linux.

%description -l pl devel
Biblioteki i pliki nag³ówkowe niezbêdne do opracowywania aplikacji ATM
dla Linuxa.

%package static
Summary:	ATM on Linux - static libraries
Summary(pl):	Obs³uga sieci ATM w Linuxie - biblioteki statyczne
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static libraries needed for development ATM applications for Linux.

%description -l pl static
Biblioteki statyczne niezbêdne do opracowywania aplikacji ATM
dla Linuxa.

%package rc-scripts
Summary:        ATM on Linux - rc-scripts
Summary(pl):    Obs³uga sieci ATM w Linuxie - skrypty startowe
Group:          Base
Requires:       %{name} = %{version}
Requires:	rc-scripts >= 0.2.9

%description rc-scripts
rc-scripts for ATM support.

%description -l pl rc-scripts
Skrypty startowe dla wsparcia obs³ugi ATM.

%prep
%setup -q -n atm -b1
install -m644 %{SOURCE2} .
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__make} depend
%{__make} CFLAGS_OPT="$RPM_OPT_FLAGS"

gcc $RPM_OPT_FLAGS -I./lib pppbr-001212-br2684ctl.c -o br2684ctl -lresolv -L./lib -latm

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{atm,sysconfig/{interfaces,network-scripts},rc.d/init.d} \
	$RPM_BUILD_ROOT/var/log/atm

%{__make} install \
	INSTROOT=$RPM_BUILD_ROOT \
	INSTPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTMAN=$RPM_BUILD_ROOT%{_mandir}

install br2684ctl $RPM_BUILD_ROOT%{_sbindir}

install config/common/hosts.atm $RPM_BUILD_ROOT%{_sysconfdir}
install config/common/e164_cc $RPM_BUILD_ROOT%{_sysconfdir}

install config/pld/atm/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/atm/
install config/pld/init.d/atm $RPM_BUILD_ROOT/etc/rc.d/init.d/
install config/pld/sysconfig/atm $RPM_BUILD_ROOT/etc/sysconfig/
install config/pld/network-scripts/{ifup-*,ifdown-*} \
		$RPM_BUILD_ROOT/etc/sysconfig/network-scripts
 
gzip -9nf doc/usage.txt BUGS CREDITS CHANGES README config/pld/README.PLD \
	config/pld/interfaces/ifcfg-*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%post rc-scripts
/sbin/chkconfig --add atm
if [ -f /var/lock/subsys/atm ]; then
	/etc/rc.d/init.d/atm restart 1>&2
fi

%preun rc-scripts
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/atm ]; then
		/etc/rc.d/init.d/atm stop 1>&2
	fi
	/sbin/chkconfig --del atm
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/usage.txt.gz *.gz
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hosts.atm
%attr(750,root,root) %dir %{_sysconfdir}/atm
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/atm/*
%config %{_sysconfdir}/e164_cc
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(751,root,root) /var/log/atm
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files rc-scripts
%defattr(644,root,root,755)
%doc config/pld/README.PLD.gz config/pld/interfaces/ifcfg-*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/atm
%attr(755,root,root) %{_sysconfdir}/sysconfig/network-scripts/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/atm
