Summary:	Netscape Portable Runtime (NSPR)
Summary(pl):	Przeno╤ne biblioteki uruchomieniowe Netscape
Name:		nspr
Version:	4.1.2
Release:	1
License:	GPL
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	Библиотеки
Group(uk):	Б╕бл╕отеки
Source0:	ftp://ftp.mozilla.org/pub/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries that implement cross-platform runtime services from
Netscape.

%description -l pl
Biblioteki z wieloplatformow╠ implementacj╠ usЁug z Netscape.

%package devel
Summary:	NSPR library header files for development
Summary(pl):	Pliki nagЁСwkowe bibliotek NSPR
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name} = %{version}

%description devel
Header files for the NSPR library from Netscape.

%description devel -l pl
Pliki nagЁСwkowe bibliotek NSPR z Netscape.

%package static
Summary:	Static NSPR library
Summary(pl):	Statyczna biblioteka NSPR
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name}-devel = %{version}

%description static
Static NSPR library.

%description static -l pl
Statyczna biblioteka NSPR.

%prep
%setup -q

%build
cd mozilla/nsprpub
%{__make} \
	DIST="$RPM_BUILD_ROOT%{_prefix}" \
	NSDISTMODE=copy \
	NS_USE_GCC=1 \
	MOZILLA_CLIENT=1 \
	NO_MDUPDATE=1 \
	USE_PTHREADS=1 \
	BUILD_OPT=1 \
	OPTIMIZER="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla/nsprpub
%{__make} \
	DIST="$RPM_BUILD_ROOT%{_prefix}" \
	NSDISTMODE=copy \
	NS_USE_GCC=1 \
	MOZILLA_CLIENT=1 \
	NO_MDUPDATE=1 \
	USE_PTHREADS=1 \
	BUILD_OPT=1 \
	OPTIMIZER="%{rpmcflags}"

install -d $RPM_BUILD_ROOT%{_includedir}/nspr
mv -f $RPM_BUILD_ROOT%{_includedir}/{*.h,nspr}
mv -f $RPM_BUILD_ROOT%{_includedir}/{obsolete,nspr}
mv -f $RPM_BUILD_ROOT%{_includedir}/{private,nspr}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/nspr

%files static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/lib*.a
