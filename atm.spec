# $Revision: 1.26 $ $Date: 2002-02-02 19:55:47 $
Summary:	ATM on Linux
Summary(pl):	Obs³uga sieci ATM w Linuxie
Name:		atm
Version:	0.62
Release:	1
License:	GPL
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe
Source0:	ftp://lrcftp.epfl.ch/pub/linux/atm/dist/%{name}-%{version}.tar.gz
Source1:	%{name}-pldrc.tar.gz
Patch0:		%{name}-opt.patch
Patch1:		%{name}-OPEN_MAX.patch
Icon:		atm-logo.gif
URL:		http://ica1www.epfl.ch/linux-atm/
Prereq:		/sbin/chkconfig
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
jeszcze w stadium alfa dzia³a ju¿ bardzo stabilnie i najprawdopodobniej
zostanie w³±czona do j±der serii 2.4.x. W Linuksie PLD sk³ada siê ona
z ³at (patches) do bie¿±cej wersji j±dra zawieraj±cych sterowniki do
kilku popularnych kart (m.in. Fore, Madge, IDT) i zapewniaj±cych
zestawianie po³±czeñ PVC i SVC oraz zestawu programów i skryptów (ten
pakiet) realizuj±cych najpopularniejsze us³ugi ATM, tj. Classical IP
(IP over ATM), klientów i serwery LAN Emulation (LANE), Multiprotocol
Over ATM (MPOA) i inne rozmaito¶ci.

%package devel
Summary:	ATM on Linux - developer's package
Summary(pl):	Obs³uga sieci ATM w Linuxie - biblioteki i pliki nag³ówkowe
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	òÁÚÒÁÂÏÔËÁ/âÉÂÌÉÏÔÅËÉ
Group(uk):	òÏÚÒÏÂËÁ/â¦ÂÌ¦ÏÔÅËÉ
Requires:	%{name} = %{version}

%description devel
Libraries and header files needed for development ATM applications for
Linux.

%description -l pl devel
Biblioteki i pliki nag³ówkowe niezbêdne do opracowywania aplikacji ATM
dla Linuksa.

%prep
%setup -q -n atm -b 1
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
 
gzip -9nf doc/usage.txt BUGS CREDITS CHANGES README config/pld/README.PLD

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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/atm/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hosts.atm
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/interfaces/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/atm
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
