Summary:	Netscape Portable Runtime (NSPR)
Summary(pl):	Przeno¶ne biblioteki uruchomieniowe Netscape
Name:		nspr
Version:	4.6
%define	snap	20041030
Release:	0.%{snap}.1
Epoch:		1
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
# :pserver:anonymous@cvs-mirror.mozilla.org:/cvsroot mozilla/nsprpub -A
# (still waiting for -r NSPR_4_6_RTM)
Source0:	%{name}-%{version}-%{snap}.tar.bz2
# Source0-md5:	b8b224d015b28ed47cbad573e0a3d363
# releases
#Source0:	http://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
Source1:	%{name}-mozilla-nspr.pc
Patch0:		%{name}-am18.patch
Patch1:		%{name}-acfix.patch
Patch2:		%{name}-libdir.patch
BuildRequires:	autoconf >= 2.12
BuildRequires:	automake
Obsoletes:	nspr-pthreads
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries that implement cross-platform runtime services from
Netscape.

%description -l pl
Biblioteki z wieloplatformow± implementacj± us³ug z Netscape.

%package devel
Summary:	NSPR library header files for development
Summary(pl):	Pliki nag³ówkowe bibliotek NSPR
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	nspr-pthreads-devel

%description devel
Header files for the NSPR library from Netscape.

%description devel -l pl
Pliki nag³ówkowe bibliotek NSPR z Netscape.

%package static
Summary:	Static NSPR library
Summary(pl):	Statyczna biblioteka NSPR
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	nspr-pthreads-static

%description static
Static NSPR library.

%description static -l pl
Statyczna biblioteka NSPR.

%prep
%setup -q -n %{name}-%{version}.HEAD
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd mozilla/nsprpub
cp -f /usr/share/automake/config.sub build/autoconf
%{__autoconf}
# don't use "--disable-strip" - it will cause stripping
%configure \
	--with-dist-prefix=$RPM_BUILD_ROOT%{_prefix} \
	--with-dist-libdir=$RPM_BUILD_ROOT%{_libdir} \
	--with-mozilla \
	--enable-optimize="%{rpmcflags}" \
	--%{?debug:en}%{!?debug:dis}able-debug \
	%{!?debug:--enable-strip} \
	--with-pthreads \
	--enable-ipv6

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_aclocaldir},%{_pkgconfigdir}}

cd mozilla/nsprpub
%{__make} install \
	NSDISTMODE=copy

install config/%{name}.m4 $RPM_BUILD_ROOT%{_aclocaldir}
install config/%{name}-config $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_pkgconfigdir}/mozilla-nspr.pc

sed -i -e 's#libdir=.*#libdir=%{_libdir}#g' \
	-e 's#includedir=.*#includedir=%{_includedir}#g' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/mozilla-nspr.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nspr-config
%{_includedir}/nspr
%{_aclocaldir}/*.m4
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
