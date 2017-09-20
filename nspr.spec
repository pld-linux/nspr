Summary:	Netscape Portable Runtime (NSPR)
Summary(pl.UTF-8):	Przenośne biblioteki uruchomieniowe Netscape
Name:		nspr
Version:	4.17
Release:	1
Epoch:		1
License:	MPL v2.0
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
# Source0-md5:	0534d9ac45dca251655b9b240670eab4
Patch0:		%{name}-pc.patch
URL:		https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSPR
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	sed >= 4.0
Obsoletes:	nspr-pthreads
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries that implement cross-platform runtime services from
Netscape.

%description -l pl.UTF-8
Biblioteki z wieloplatformową implementacją usług
uruchomieniowych Netscape'a.

%package devel
Summary:	NSPR library header files for development
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek NSPR
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	nspr-pthreads-devel

%description devel
Header files for the NSPR library from Netscape.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek NSPR Netscape'a.

%package static
Summary:	Static NSPR library
Summary(pl.UTF-8):	Statyczna biblioteka NSPR
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	nspr-pthreads-static

%description static
Static NSPR library.

%description static -l pl.UTF-8
Statyczna biblioteka NSPR.

%prep
%setup -q
%patch0 -p1

%build
cd nspr
cp -f /usr/share/automake/config.sub build/autoconf
%{__autoconf}
%configure \
	--includedir=%{_includedir}/nspr \
%ifarch %{x8664} ppc64
	--enable-64bit \
%endif
%ifarch x32
	--enable-x32 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug \
	--enable-ipv6 \
	--enable-optimize="%{rpmcflags}" \
	--with-mozilla \
	--with-pthreads

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C nspr install \
	DESTDIR=$RPM_BUILD_ROOT

# for compatibility (upstream installs only nspr.nc); to be dropped sometime?
ln -s nspr.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/mozilla-nspr.pc

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{compile-et.pl,prerr.properties}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnspr4.so
%attr(755,root,root) %{_libdir}/libplc4.so
%attr(755,root,root) %{_libdir}/libplds4.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nspr-config
%{_includedir}/nspr
%{_aclocaldir}/nspr.m4
%{_pkgconfigdir}/mozilla-nspr.pc
%{_pkgconfigdir}/nspr.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnspr4.a
%{_libdir}/libplc4.a
%{_libdir}/libplds4.a
