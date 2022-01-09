#
# Conditional build:
%bcond_without	ocaml_opt	# build opt (native code)

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	easy-format
Summary:	easy(ier) pretty printing for OCaml
Summary(pl.UTF-8):	Łatwiejsze ładne wypisywanie dla OCamla
Name:		ocaml-%{module}
Version:	1.3.2
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/ocaml-community/easy-format/releases
Source0:	https://github.com/ocaml-community/easy-format/releases/download/%{version}/%{module}-%{version}.tbz
# Source0-md5:	8e8e2da60d3566ab1bce5e5784ae75f9
# https://github.com/ocaml-community/easy-format/commit/c6d5ab5ef62e7a1ec20ae8a22a39b0f06ad710a8.patch
Patch0:		%{name}-compile.patch
URL:		https://github.com/ocaml-community/easy-format
BuildRequires:	ocaml >= 1:4.02.3
BuildRequires:	ocaml-dune >= 1.10
BuildRequires:	ocaml-findlib
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
Summary(pl.UTF-8):	Wiązania easy-format dla OCamla - część programistyczna
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
%patch0 -p1

%build
dune build @all %{?_smp_mflags} --display=verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# just sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}/easy_format.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/%{module}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE README.md
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%{_libdir}/ocaml/%{module}/easy_format.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/easy_format.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/dune-package
%{_libdir}/ocaml/%{module}/opam
%{_libdir}/ocaml/%{module}/easy_format.cmi
%{_libdir}/ocaml/%{module}/easy_format.cmt*
# doc?
%{_libdir}/ocaml/%{module}/easy_format.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/easy_format.a
%{_libdir}/ocaml/%{module}/easy_format.cmx
%{_libdir}/ocaml/%{module}/easy_format.cmxa
%endif
