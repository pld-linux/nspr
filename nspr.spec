Summary:	Netscape Portable Runtime (NSPR)
Summary(pl):	Przeno¶ne biblioteki uruchomieniowe Netscape
Name:		nspr
Version:	4.2.2
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://ftp.mozilla.org/pub/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
Patch0:		%{name}-alpha.patch
BuildRequires:	autoconf
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
Requires:	%{name} = %{version}
Obsoletes:	nspr-pthreads-devel

%description devel
Header files for the NSPR library from Netscape.

%description devel -l pl
Pliki nag³ówkowe bibliotek NSPR z Netscape.

%package static
Summary:	Static NSPR library
Summary(pl):	Statyczna biblioteka NSPR
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Obsoletes:	nspr-pthreads-static

%description static
Static NSPR library.

%description static -l pl
Statyczna biblioteka NSPR.

%prep
%setup -q
#%patch -p1

%build
cd mozilla/nsprpub
%{__autoconf}
%configure \
	--with-dist-prefix=$RPM_BUILD_ROOT%{_prefix} \
	--with-mozilla \
	--enable-optimize="%{rpmcflags}" \
	--disable-debug \
	--enable-strip \
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
