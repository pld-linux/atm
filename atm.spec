# $Revision: 1.9 $ $Date: 2000-01-12 15:54:43 $
Summary:	ATM on Linux
Summary(pl):	Obs³uga sieci ATM w Linuxie
Name:		atm
Version:	0.62
Release:	1
Copyright:	GPL
Group:		Networking
Group(pl):	Sieciowe
Source0:	ftp://lrcftp.epfl.ch/pub/linux/atm/dist/atm-%{version}.tar.gz
Source1:	atm-pldrc.tar.gz
Patch:		atm-opt.patch
Icon:		atm-logo.gif
URL:		http://ica1www.epfl.ch/linux-atm/
Buildroot:	/tmp/%{name}-%{version}-root
 
%description
ATM (Asynchronous Transfer Mode) networking for Linux is still under 
development now but it works quite stable now and will most probably be 
included in 2.4.x series kernels. In PLD Linux it consists of some patches 
for current kernel version containing drivers for a few popular ATM cards
(ex. Fore, Madge, IDT) and PVC and SVC support. It also includes programs
and scripts providing the most popular ATM services, i.e. Classical IP (IP
over ATM), LAN Emulation clients and servers, Multiprotocol Over ATM 
(MPOA) and some other goodies.

%description -l pl
Obs³uga sieci ATM (Asynchronous Transfer Mode) w Linuxie mimo i¿ jest jeszcze
w stadium alfa dzia³a ju¿ bardzo stabilnie i najproawdopodobniej zostanie
w³±czona do j±der serii 2.4.x. W Linuxie PLD sk³ada siê ona z ³at (patches) do
bie¿±cej wersji j±dra zawieraj±cych sterowniki do kilku popularnych kart (m.in 
Fore, Madge, IDT) i zapewniaj±cych zestawianie po³±czeñ PVC i SVC oraz zestawu 
programów i skryptów (ten pakiet) realizuj±cych najpopularniejsze us³ugi
ATM, tj. Classical IP (IP over ATM), klientów i serwery LAN Emulation (LANE),
Multiprotocol Over ATM (MPOA) i inne rozmaito¶ci.

%package devel
Summary:	ATM on Linux - developer's package
Summary(pl):	Obs³uga sieci ATM w Linuxie - biblioteki i pliki nag³ówkowe
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Libraries and header files needed for development ATM applications for Linux

%description -l pl devel
Biblioteki i pliki nag³ówkowe niezbêdne do opracowywania aplikacji ATM dla
Linuxa.

%prep
%setup -q -n atm -b 1
%patch0 -p1

%build
make depend
make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{atm,sysconfig/{interfaces,network-scripts},rc.d/init.d} \
	$RPM_BUILD_ROOT/var/log/atm

make install \
	INSTROOT=$RPM_BUILD_ROOT \
	INSTPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTMAN=$RPM_BUILD_ROOT%{_mandir}

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/*

install config/common/hosts.atm $RPM_BUILD_ROOT/etc
install config/common/e164_cc $RPM_BUILD_ROOT/etc

install config/pld/atm/* $RPM_BUILD_ROOT/etc/atm/
install config/pld/init.d/atm $RPM_BUILD_ROOT/etc/rc.d/init.d/
install config/pld/sysconfig/atm $RPM_BUILD_ROOT/etc/sysconfig/
install config/pld/network-scripts/{ifup-atm,ifup-lec,ifdown-atm,ifdown-lec} \
	$RPM_BUILD_ROOT/etc/sysconfig/network-scripts
install config/pld/interfaces/{ifcfg-atm0,ifcfg-lec0} \
	$RPM_BUILD_ROOT/etc/sysconfig/interfaces 
 
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	doc/usage.txt BUGS CREDITS CHANGES README config/pld/README.PLD
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755) 
%doc doc/usage.txt.gz *.gz config/pld/README.PLD.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%config /etc/e164_cc
%config(noreplace) /etc/hosts.atm
%attr(755,root,root) %config /etc/sysconfig/network-scripts/*
%attr(754,root,root) %config /etc/rc.d/init.d/atm
%attr(640,root,root) %config /etc/sysconfig/atm
%config /etc/atm/*
%config(noreplace) /etc/sysconfig/interfaces/*
%dir /var/log/atm
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755) 
/usr/include/*
/usr/lib/*
