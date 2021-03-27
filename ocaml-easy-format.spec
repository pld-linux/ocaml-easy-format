#
# Conditional build:
%bcond_without	ocaml_opt	# build opt (native code)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	easy-format
Summary:	easy(ier) pretty printing for OCaml
Summary(pl.UTF-8):	Łatwiejsze ładne wypisywanie dla OCamla
Name:		ocaml-%{module}
Version:	1.0.2
Release:	9
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
easy-format module offers a simplified interface to the Format module
of the OCaml standard library. Input data must be converted into a
tree using 3 kinds of nodes: atoms, lists and labelled nodes. Each
node is bound to its own formatting parameters and a single function
call produces the formatted output.

%description -l pl.UTF-8
Moduł easy-format oferuje uproszczony interfejs do modułu Format
biblioteki standardowej OCamla. Dane wejściowe muszą być
przekonwertowane do drzewa z użyciem trzech rodzajów węzłów: atomów,
list oraz węzłów z etykietami. Każdy węzeł jest powiązany z
parametrami formatującymi, a pojedyncze wywołanie funkcji tworzy
sformatowane wyjście.

%package devel
Summary:	easy-format binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania easy-format dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml
Requires:	%{name} = %{version}-%{release}

%description devel
easy-format module offers a simplified interface to the Format module
of the OCaml standard library. Input data must be converted into a
tree using 3 kinds of nodes: atoms, lists and labelled nodes. Each
node is bound to its own formatting parameters and a single function
call produces the formatted output.

This package contains files needed to develop OCaml programs using
easy-format library.

%description devel -l pl.UTF-8
Moduł easy-format oferuje uproszczony interfejs do modułu Format
biblioteki standardowej OCamla. Dane wejściowe muszą być
przekonwertowane do drzewa z użyciem trzech rodzajów węzłów: atomów,
list oraz węzłów z etykietami. Każdy węzeł jest powiązany z
parametrami formatującymi, a pojedyncze wywołanie funkcji tworzy
sformatowane wyjście.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki easy-format.

%prep
%setup -q -n %{module}-%{version}

%build
%{__make} -j1 all %{?with_ocaml_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR/stublibs

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%{_libdir}/ocaml/%{module}/easy_format.cmo
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/easy_format.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc README.md Changes LICENSE
%{_libdir}/ocaml/%{module}/easy_format.cmi
# doc?
%{_libdir}/ocaml/%{module}/easy_format.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/easy_format.o
%{_libdir}/ocaml/%{module}/easy_format.cmx
%endif
