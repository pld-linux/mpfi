#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests
#
Summary:	Multiple-precision floating-point interval library
Summary(pl.UTF-8):	Biblioteka przedziałów zmiennoprzecinkowych wielokrotnej precyzji
Name:		mpfi
Version:	1.5.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://perso.ens-lyon.fr/nathalie.revol/softwares/%{name}-%{version}.tar.xz
# Source0-md5:	efff5c254d1af49f42ed75cbcd9166db
Patch0:		%{name}-info.patch
Patch1:		%{name}-missing.patch
URL:		http://perso.ens-lyon.fr/nathalie.revol/software.html
BuildRequires:	gmp-devel >= 4.1
BuildRequires:	mpfr-devel >= 4.0.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
Requires:	gmp >= 4.1
Requires:	mpfr >= 4.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MPFI is intended to be a portable library written in C for arbitrary
precision interval arithmetic with intervals represented using MPFR
reliable floating-point numbers. It is based on the GNU MP library and
on the MPFR library. The purpose of an arbitrary precision interval
arithmetic is on the one hand to get guaranteed results, thanks to
interval computation, and on the other hand to obtain accurate
results, thanks to multiple precision arithmetic. The MPFI library is
built upon MPFR in order to benefit from the correct rounding
provided, for each operation or function, by MPFR. Further advantages
of using MPFR are its portability and compliance with the IEEE 754
standard for floating-point arithmetic.

%description -l pl.UTF-8
MPFI jest przenośną, napisaną w C biblioteką do obliczeń na
przedziałach dowolnej precyzji, z przedziałami reprezentowanymi przy
użyciu niezawodnych liczby zmiennoprzecinkowych MPFR. Jest oparta na
bibliotekach GNU MP i MPFR. Celem arytmetyki na przedziałach dowolnej
precyzji jest gwarancja wyników, dzięki obliczeniom przedziałów, a
także dokładność wyników, dzięki arytmetyce wielokrotnej precyzji.
Biblioteka MPFI jest zbudowana w oparciu o MPFR, aby wykorzystać
poprawne zaokrąglenia przy każdej operacji lub funkcji wykonywanej
przez MPFR. Inne zalety MPFR to przenośność i zgodność ze standardem
IEEE 754 dla arytmetyki zmiennoprzecinkowej.

%package devel
Summary:	Header files for MPFI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MPFI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gmp-devel >= 4.1
Requires:	mpfr-devel >= 4.0.1

%description devel
Header files for MPFI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MPFI.

%package static
Summary:	Static MPFI library
Summary(pl.UTF-8):	Statyczna biblioteka MPFI
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MPFI library.

%description static -l pl.UTF-8
Statyczna biblioteka MPFI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmpfi.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/mpfi

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libmpfi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmpfi.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmpfi.so
%{_includedir}/mpfi.h
%{_includedir}/mpfi_io.h
%{_pkgconfigdir}/mpfi.pc
%{_infodir}/mpfi.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmpfi.a
