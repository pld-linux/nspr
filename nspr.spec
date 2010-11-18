Summary:	Netscape Portable Runtime (NSPR)
Summary(pl.UTF-8):	Przenośne biblioteki uruchomieniowe Netscape
Name:		nspr
Version:	4.8.6
Release:	2
Epoch:		1
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
# Source0-md5:	592c275728c29d193fdba8009165990b
Source1:	%{name}-mozilla-nspr.pc
Patch0:		%{name}-acfix.patch
Patch1:		%{name}-sparc64.patch
URL:		http://www.mozilla.org/projects/nspr/
BuildRequires:	autoconf >= 2.12
BuildRequires:	automake
BuildRequires:	sed >= 4.0
Obsoletes:	nspr-pthreads
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries that implement cross-platform runtime services from
Netscape.

%description -l pl.UTF-8
Biblioteki z wieloplatformową implementacją usług z Netscape.

%package devel
Summary:	NSPR library header files for development
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek NSPR
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	nspr-pthreads-devel

%description devel
Header files for the NSPR library from Netscape.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek NSPR z Netscape.

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
%patch1 -p0

install %{SOURCE1} mozilla/nsprpub/nspr-mozilla-nspr.pc.in

%build
cd mozilla/nsprpub
cp -f /usr/share/automake/config.sub build/autoconf
%{__autoconf}
%configure \
	--includedir=%{_includedir}/nspr \
%ifarch %{x8664} ppc64
	--enable-64bit \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug \
	--enable-ipv6 \
	--enable-optimize="%{rpmcflags}" \
	--with-mozilla \
	--with-pthreads

%{__make}

./config.status --file=nspr-mozilla-nspr.pc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} -C mozilla/nsprpub install \
	DESTDIR=$RPM_BUILD_ROOT

install mozilla/nsprpub/nspr-mozilla-nspr.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/mozilla-nspr.pc

ln -s mozilla-nspr.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/nspr.pc

rm $RPM_BUILD_ROOT%{_bindir}/{compile-et.pl,prerr.properties}

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
