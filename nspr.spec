Summary:	Netscape Portable Runtime (NSPR)
Summary(pl):	Przeno¶ne biblioteki uruchomieniowe Netscape
Name:		nspr
# it's actually 4.5, but leave this .0 because of previous snaps
Version:	4.5.0
Release:	1
Epoch:		1
License:	MPL or GPL
Group:		Libraries
# :pserver:anonymous@cvs-mirror.mozilla.org:/cvsroot mozilla/nsprpub -r NSPR_4_5_RTM
Source0:	%{name}-4.5.tar.bz2
# Source0-md5:	f4bfd5d90ff9ddfcb58bf2b9a1704f91
#Source0:	http://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
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
%setup -q -n %{name}-4.5
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
install -d $RPM_BUILD_ROOT%{_aclocaldir}

cd mozilla/nsprpub
%{__make} install \
	NSDISTMODE=copy

install config/%{name}.m4 $RPM_BUILD_ROOT%{_aclocaldir}
install config/%{name}-config $RPM_BUILD_ROOT%{_bindir}

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

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
