# $Revision: 1.6 $ $Date: 1999-11-08 19:46:37 $
Summary:	ATM on Linux
Summary(pl):	Obs³uga sieci ATM w Linuxie
Name:		ATM
Version:	0.62
Release:	1
Copyright:	GPL
Group:		Networking
Group(pl):	Sieciowe
Source0		ftp://lrcftp.epfl.ch/pub/linux/atm/dist/atm-%{version}.tar.gz
Source1:	ATM-pldrc.tar.gz
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
Group:		Development
Group(pl):	Programowanie
Requires:	%{name} = %{version}

%description devel
Libraries and header files needed for development ATM applications for Linux

%description -l pl devel
Biblioteki i pliki nag³ówkowe niezbêdne do opracowywania aplikacji ATM dla
Linuxa.

%prep
%setup -q -n atm -b 1

%build
make depend
make 

%install
rm -rf $RPM_BUILD_ROOT

make \
    INSTROOT=$RPM_BUILD_ROOT \
    INSTPREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTMAN=$RPM_BUILD_ROOT%{_mandir} \
    install

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* 
gzip -9nf doc/usage.txt BUGS CREDITS CHANGES README config/pld/README.PLD

install -d -m 0755 $RPM_BUILD_ROOT/etc 
install -c -m 0644 config/common/hosts.atm $RPM_BUILD_ROOT/etc
install -c -m 0644 config/common/e164_cc $RPM_BUILD_ROOT/etc

install -d -m 0755 $RPM_BUILD_ROOT/etc/atm
install -d -m 0755 $RPM_BUILD_ROOT/etc/sysconfig
install -d -m 0755 $RPM_BUILD_ROOT/etc/sysconfig/network-scripts
install -d -m 0755 $RPM_BUILD_ROOT/etc/sysconfig/interfaces
install -d -m 0755 $RPM_BUILD_ROOT/etc/rc.d/init.d
install -c -m 0644 config/pld/atm/* $RPM_BUILD_ROOT/etc/atm/
install -c -m 0755 config/pld/init.d/atm $RPM_BUILD_ROOT/etc/rc.d/init.d/
install -c -m 0644 config/pld/sysconfig/atm $RPM_BUILD_ROOT/etc/sysconfig/
install -c -m 0755 config/pld/network-scripts/{ifup-atm,ifup-lec,ifdown-atm,ifdown-lec} \
	$RPM_BUILD_ROOT/etc/sysconfig/network-scripts
install -c -m 0644 config/pld/interfaces/{ifcfg-atm0,ifcfg-lec0} \
	$RPM_BUILD_ROOT/etc/sysconfig/interfaces 
install -d $RPM_BUILD_ROOT/var/log/atm
 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755) 
%doc doc/usage.txt.gz *.gz config/pld/README.PLD.gz
%{_mandir}/man*/*
%config /etc/e164_cc
%config(noreplace) /etc/hosts.atm
%attr(755,root,root) %config /etc/sysconfig/network-scripts/*
%attr(755,root,root) %config /etc/rc.d/init.d/atm
%config /etc/sysconfig/atm
%config /etc/atm/*
%config(noreplace) /etc/sysconfig/interfaces/*
%attr(755,root,root) /var/log/atm
%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/sbin/*

%files devel
%defattr(644,root,root,755) 
/usr/include/*
/usr/lib/*
