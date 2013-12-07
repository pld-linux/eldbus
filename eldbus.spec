# NOTE: for versions >= 1.8 see efl.spec
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		ecore_ver	1.7.9
%define		eina_ver	1.7.9

Summary:	Easy access to D-Bus from EFL applications
Summary(pl.UTF-8):	Łatwy dostęp do usługi D-Bus z aplikacji EFL
Name:		eldbus
Version:	1.7.9
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	f86ddcdfbb3a3df5654e72940cd7c0b5
URL:		http://git.enlightenment.org/legacy/eldbus.git/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1.6
BuildRequires:	dbus-devel
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	eina-devel >= %{eina_ver}
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.22
Requires:	ecore >= %{ecore_ver}
Requires:	eina >= %{eina_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
Eldbus provides easy access to D-Bus from EFL applications.

Eldbus allows connecting to both system and session buses acting as
both client and service roles.

%description -l pl.UTF-8
Eldbus zapewnia łatwy dostęp do usługi D-Bus z aplikacji EFL.

Eldbus pozwala na łączenie się z szyną systemową lub sesyjną, zarówno
w roli klienta, jak i usługi.

%package devel
Summary:	Header files for eldbus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki eldbus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus-devel
Requires:	ecore-devel >= %{ecore_ver}
Requires:	eina-devel >= %{eina_ver}

%description devel
Header files for eldbus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki eldbus.

%package static
Summary:	Static eldbus library
Summary(pl.UTF-8):	Statyczna biblioteka eldbus
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static eldbus library.

%description static -l pl.UTF-8
Statyczna biblioteka eldbus.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libeldbus.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libeldbus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeldbus.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/eldbus-codegen
%attr(755,root,root) %{_libdir}/libeldbus.so
%{_includedir}/eldbus-1
%{_pkgconfigdir}/eldbus.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeldbus.a
%endif
