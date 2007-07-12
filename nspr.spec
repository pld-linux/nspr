Summary:	Netscape Portable Runtime (NSPR)
Summary(pl.UTF-8):	Przenośne biblioteki uruchomieniowe Netscape
Name:		nspr
Version:	4.6.7
Release:	1
Epoch:		1
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
# Source0-md5:	75d5de21ebc1a21886a25673920490ff
Source1:	%{name}-mozilla-nspr.pc
Patch0:		%{name}-am18.patch
Patch1:		%{name}-acfix.patch
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
%patch1 -p1

# @includedir@ is not updated to .../nspr
sed -i -e 's,@includedir@,%{_includedir}/nspr,' mozilla/nsprpub/config/nspr-config.in

%build
cd mozilla/nsprpub
cp -f /usr/share/automake/config.sub build/autoconf
%{__autoconf}
# don't use "--disable-strip" - it will cause stripping
%configure \
	--with-dist-prefix=$RPM_BUILD_ROOT%{_prefix} \
	--with-dist-libdir=$RPM_BUILD_ROOT%{_libdir} \
	--with-mozilla \
%ifarch %{x8664} ppc64
	--enable-64bit \
%endif
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

sed \
	-e 's#libdir=.*#libdir=%{_libdir}#g' \
	-e 's#includedir=.*#includedir=%{_includedir}#g' \
	-e 's#VERSION#%{version}#g' \
	%{SOURCE1} > $RPM_BUILD_ROOT%{_pkgconfigdir}/mozilla-nspr.pc

ln -s mozilla-nspr.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/nspr.pc

# let rpm find deps
chmod 755 $RPM_BUILD_ROOT%{_libdir}/lib*.so

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
%{_libdir}/lib*.a
