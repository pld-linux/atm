# $Revision: 1.13.2.5 $ $Date: 2000-11-04 05:21:46 $
Summary:	ATM on Linux
Summary(pl):	Obs³uga sieci ATM w Linuxie
Name:		atm
Version:	0.78
Release:	2
License:	GPL
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe
URL:		http://ica1www.epfl.ch/linux-atm/
Source0:	ftp://lrcftp.epfl.ch/pub/linux/atm/dist/%{name}-%{version}.tar.gz
Source1:	%{name}-0.78-PLDrc.tar.gz
Patch0:		%{name}-opt.patch
Patch1:		%{name}-OPEN_MAX.patch
Icon:		atm-logo.gif
Requires:	rc-scripts > 0.2.7
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
Linux

%description -l pl devel
Biblioteki i pliki nag³ówkowe niezbêdne do opracowywania aplikacji ATM
dla Linuxa.

%prep
%setup -q -n atm -b 1
%patch0 -p1
%patch1 -p1

%build
# Test it before removing!
# gcc 2.95.x with optimizations turned on miscompiles atm 0.62!!!
#RPM_OPT_FLAGS=""
#export RPM_OPT_FLAGS
%{__make} depend
%{__make} CFLAGS_OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{atm,sysconfig/{interfaces,network-scripts},rc.d/init.d} \
	$RPM_BUILD_ROOT/var/log/atm

%{__make} install \
	INSTROOT=$RPM_BUILD_ROOT \
	INSTPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTMAN=$RPM_BUILD_ROOT%{_mandir}

install config/common/hosts.atm $RPM_BUILD_ROOT%{_sysconfdir}
install config/common/e164_cc $RPM_BUILD_ROOT%{_sysconfdir}

install config/pld/atm/{*.conf,services} $RPM_BUILD_ROOT%{_sysconfdir}/atm/
install config/pld/init.d/atm $RPM_BUILD_ROOT/etc/rc.d/init.d/
install config/pld/sysconfig/atm $RPM_BUILD_ROOT/etc/sysconfig/
install config/pld/network-scripts/{ifup-*,ifdown-*} \
		$RPM_BUILD_ROOT/etc/sysconfig/network-scripts
 
gzip -9nf doc/usage.txt BUGS CREDITS CHANGES README config/pld/README.PLD \
	config/pld/interfaces/ifcfg-*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add atm
if [ -f /var/lock/subsys/atm ]; then
	/etc/rc.d/init.d/atm restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/atm ]; then
		/etc/rc.d/init.d/atm stop 1>&2
	fi
	/sbin/chkconfig --del atm
fi

%files
%defattr(644,root,root,755)
%doc doc/usage.txt.gz *.gz config/pld/README.PLD.gz
%doc config/pld/interfaces/ifcfg-*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/atm/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hosts.atm
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/atm
%attr(755,root,root) %{_sysconfdir}/sysconfig/network-scripts/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/atm
%config %{_sysconfdir}/e164_cc
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(751,root,root) /var/log/atm
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/*
