#
# Conditional build:
%bcond_without	opt		# build opt

%define		module	easy-format
Summary:	easy(ier) pretty printing for OCaml
Name:		ocaml-%{module}
Version:	1.0.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://mjambon.com/releases/easy-format/%{module}-%{version}.tar.gz
# Source0-md5:	82f6db85477831cab11e4cfe80321225
URL:		http://mjambon.com/easy-format.html
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
This module offers a simplified interface to the Format module of the
OCaml standard library. Input data must be converted into a tree using
3 kinds of nodes: atoms, lists and labelled nodes. Each node is bound
to its own formatting parameters and a single function call produces
the formatted output.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	easy-format binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania easy-format dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n %{module}-%{version}

%build
%{__make} -j1 all %{?with_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $OCAMLFIND_DESTDIR/%{module}/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc README.md Changes LICENSE
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/*.cm[xi]
%{_libdir}/ocaml/%{module}/*.cmo
%{_libdir}/ocaml/%{module}/*.mli
%if %{with opt}
%{_libdir}/ocaml/%{module}/*.o
%endif
%{_libdir}/ocaml/site-lib/%{module}
