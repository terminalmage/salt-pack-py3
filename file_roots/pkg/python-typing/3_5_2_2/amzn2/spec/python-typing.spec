%bcond_with python2
%bcond_without python3
%bcond_with tests

%{!?python3_pkgversion:%global python3_pkgversion 3}
%if ( "0%{?dist}" == "0.amzn2" )
%global with_amzn2 1
%endif

Name:           python-typing
Version:        3.5.2.2
Release:        5%{?dist}
Summary:        Typing defines a standard notation for type annotations
License:        Python
URL:            https://pypi.python.org/pypi/typing
Source0:        https://files.pythonhosted.org/packages/source/t/typing/typing-%{version}.tar.gz
BuildArch:      noarch

%description
Typing defines a standard notation for Python function and variable type
annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime
type checkers, static analyzers, IDEs and other tools.


%if %{with python2}
%package -n python2-typing
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_amzn2}
BuildRequires:  python2-rpm-macros
%endif
%{?python_provide:%python_provide python2-typing}

%description -n python2-typing
Typing defines a standard notation for Python function and variable type
annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime
type checkers, static analyzers, IDEs and other tools.
%endif


%if %{with python3}
%package -n python%{python3_pkgversion}-typing
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if 0%{?with_amzn2}
BuildRequires:  python3-rpm-macros
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-typing}

%description -n python%{python3_pkgversion}-typing
Typing defines a standard notation for Python function and variable type
annotations. The notation can be used for documenting code in a concise,
standard format, and it has been designed to also be used by static and runtime
type checkers, static analyzers, IDEs and other tools.
%endif


%prep
%setup -qc
%if %{with python2}
mv typing-%{version} python2
cp -al python2/{README.rst,LICENSE} .
%endif
%if %{with python3}
mv typing-%{version} python3
cp -al python3/{README.rst,LICENSE} .
%endif

%build
%if %{with python2}
cd python2
%{py2_build}
cd -
%endif
%if %{with python3}
cd python3
## %%py3_build
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} build --executable="%{__python3} %{py3_shbang_opts}" %{?*}
sleep 1
cd -
%endif

%install
%if %{with python2}
cd python2
%{py2_install}
cd -
%endif
%if %{with python3}
cd python3
## %%py3_install
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot} %{?*}
cd -
%endif

%if %{with python2}
%files -n python2-typing
%doc README.rst
%license LICENSE
%{python2_sitelib}/typing*
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-typing
%doc README.rst
%license LICENSE
%{python3_sitelib}/typing*
%{python3_sitelib}/__pycache__/typing*
%endif

%changelog
* Mon Jun 17 2019 SaltStack Packaging Team <packaging@saltstack.com> - 3.5.2.2-5
- Made support for Python 2 optional

* Wed Oct 03 2018 SaltStack Packaging Team <packaging@saltstack.com> - 3.5.2.2-4
- Updated to allow for Amazon Linux 2 Python 3 support

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-3
- Bump release to supercede previous python2-typing

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-2
- Build python2/3 separately to ensure proper install

* Mon Jan 23 2017 Orion Poplawski <orion@cora.nwra.com> - 3.5.2.2-1
- Initial EPEL package
