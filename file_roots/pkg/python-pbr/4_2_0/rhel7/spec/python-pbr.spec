%global pypi_name pbr


%bcond_with python2
%bcond_without python3
%bcond_with tests
%bcond_with docs

Name:           python-%{pypi_name}
Version:        4.2.0
Release:        4%{?dist}
Summary:        Python Build Reasonableness

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/pbr
Source0:        https://pypi.io/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch


%description
PBR is a library that injects some useful and sensible default behaviors into
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18
different projects each with at least 3 active branches, it seems like a good
time to make that code into a proper re-usable library.

%if %{with python2}
%package -n python2-%{pypi_name}
Summary:        Python Build Reasonableness
%if %{with python2} && %{with docs}
BuildRequires: python2-sphinx >= 1.1.3
BuildRequires: python2-oslo-sphinx
%endif
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with tests}
BuildRequires:  python2-coverage
BuildRequires:  python2-hacking
BuildRequires:  python2-mock
BuildRequires:  python2-testrepository
BuildRequires:  python2-testresources
BuildRequires:  python2-testscenarios
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  gnupg
%endif
Requires:       python2-setuptools
Requires:       git-core

%description -n python2-%{pypi_name}
Manage dynamic plugins for Python applications
%endif


%if %{with python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        Python Build Reasonableness
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-setuptools
Requires:       git-core

%description -n python%{python3_pkgversion}-%{pypi_name}
Manage dynamic plugins for Python applications

%if 0%{?python3_other_pkgversion}
%package -n python%{python3_other_pkgversion}-%{pypi_name}
Summary:        Python Build Reasonableness
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{pypi_name}}

BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-setuptools
Requires:       python%{python3_other_pkgversion}-setuptools
Requires:       git-core

%description -n python%{python3_other_pkgversion}-%{pypi_name}
Manage dynamic plugins for Python applications
%endif
%endif

%prep
%setup -q -n %{pypi_name}-%{version}

rm -rf {test-,}requirements.txt pbr.egg-info/requires.txt


%build
export SKIP_PIP_INSTALL=1
%if %{with python2}
%py2_build
%endif

%if %{with python3}
%py3_build
%if 0%{?python3_other_pkgversion}
%py3_other_build
%endif
%endif

%if %{with docs}
# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif


%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
%py3_install
rm -rf %{buildroot}%{python3_sitelib}/pbr/tests
mv %{buildroot}%{_bindir}/pbr %{buildroot}%{_bindir}/pbr-%{python3_version}
%if 0%{?python3_other_pkgversion}
%py3_other_install
rm -rf %{buildroot}%{python3_other_sitelib}/pbr/tests
mv %{buildroot}%{_bindir}/pbr %{buildroot}%{_bindir}/pbr-%{python3_other_version}
%endif
%endif

%if %{with python2}
%py2_install
rm -rf %{buildroot}%{python2_sitelib}/pbr/tests
%endif

%if %{with tests}
%check
%{__python2} setup.py test
%endif

%if %{with python2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc html README.rst
%{_bindir}/pbr
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/%{pypi_name}
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-pbr
%license LICENSE
## %%doc html README.rst
%doc README.rst
%{_bindir}/pbr-%{python3_version}
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}

%if 0%{?python3_other_pkgversion}
%files -n python%{python3_other_pkgversion}-pbr
%license LICENSE
## %%doc html README.rst
%doc README.rst
%{_bindir}/pbr-%{python3_other_version}
%{python3_other_sitelib}/*.egg-info
%{python3_other_sitelib}/%{pypi_name}
%endif
%endif

%changelog
* Sun Sep 22 2019 SaltStack Packaging Team <packaging@saltstack.com> - 4.2.0-4
- Made support for Python 2 packages and tests and doc optional

* Fri Mar 08 2019 Troy Dawson <tdawson@redhat.com> - 4.2.0-3
- Rebuilt to change main python from 3.4 to 3.6

* Sat Nov  3 2018 Orion Poplwski <orion@nwra.com> - 4.2.0-2
- Build for Python 3 for EPEL

* Tue Sep 04 2018 Matthias Runge <mrunge@redhat.com> - 4.2.0-1
- update to 4.2.0 (rhbz#1605192)

* Wed Aug  8 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.1-2
- Add runtime requirement to git-core

* Fri Jul 20 2018 Matthias Runge <mrunge@redhat.com> - 4.1.1-1
- rebase to 4.1.1 (rhbz#1605192)

* Wed Jul 18 2018 Haïkel Guémar  <hguemar@fedoraproject.org> - 4.1.0-2
- Add dependency to setuptools (RHBZ#1601767)

* Tue Jul 17 2018 Matthias Runge <mrunge@redhat.com> - 4.1.0-1
- update to 4.1.0 (rhbz#1561252)
- modernize spec

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-8
- Rebuilt for Python 3.7

* Tue Feb 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.1.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 15 2018 Tomas Orsava <torsava@redhat.com> - 3.1.1-6
- Switch %%python macro to %%python2

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 3.1.1-4
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Jan Beran <jberan@redhat.com> 3.1.1-2
- Fix of missing Python 3 version of executables in python3-pbr subpackage

* Wed Jun 28 2017 Alan Pevec <alan.pevec@redhat.com> 3.1.1-1
- Update to 3.1.1

* Fri Mar  3 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 2.0.0-1
- Upstream 2.0.0
- Drop upstreamed patch

* Sat Feb 18 2017 Alan Pevec <apevec AT redhat.com> - 1.10.0-4
- Fix newer Sphinx and Python 3.5 support LP#1379998

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.10.0-2
- Rebuild for Python 3.6

* Wed Oct 12 2016 Alan Pevec <apevec AT redhat.com> - 1.10.0-1
- Update to 1.10.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4 2016 Paul Belanger <pabelanger@redhat.com> 1.8.1-3
- Provide python2-pbr (rhbz#1282126)
- minor spec cleanup

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 12 2015 Alan Pevec <alan.pevec@redhat.com> 1.8.1-1
- Update to 1.8.1

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 14 2015 Alan Pevec <alan.pevec@redhat.com> 1.8.0-1
- Update to upstream 1.8.0

* Tue Sep 08 2015 Alan Pevec <alan.pevec@redhat.com> 1.7.0-1
- Update to upstream 1.7.0

* Mon Aug 31 2015 Matthias Runge <mrunge@redhat.com> - 1.6.0-1
- update to upstream 1.6.0 (rhbz#1249840)

* Sat Aug 15 2015 Alan Pevec <alan.pevec@redhat.com> 1.5.0-1
- Update to upstream 1.5.0

* Wed Jul 15 2015 Alan Pevec <alan.pevec@redhat.com> 1.3.0-1
- Update to upstream 1.3.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Alan Pevec <apevec@redhat.com> - 0.11.0-1
- update to 0.11.0

* Fri Mar 20 2015 Alan Pevec <apevec@redhat.com> - 0.10.8-1
- update to 0.10.8

* Mon Dec 29 2014 Alan Pevec <apevec@redhat.com> - 0.10.7-1
- update to 0.10.7

* Tue Nov 25 2014 Matthias Runge <mrunge@redhat.com> - 0.10.0-1
- update to 0.10.0 (rhbz#1191232)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 30 2014 Matthias Runge <mrunge@redhat.com> - 0.8.0-1
- update to 0.8.0 (rhbz#1078761)

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-2
- Added python3 subpackage.
- slight modification of Ralph Beans proposal

* Mon Mar 24 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-1
- update to 0.7.0 (rhbz#1078761)

* Tue Feb 11 2014 Matthias Runge <mrunge@redhat.com> - 0.6.0-1
- update to 0.6.0 (rhbz#1061124)

* Fri Nov 01 2013 Matthias Runge <mrunge@redhat.com> - 0.5.23-1
- update to 0.5.23 (rhbz#1023926)

* Tue Aug 13 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-2
- add requirement python-pip (rhbz#996192)
- remove requirements.txt

* Thu Aug 08 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-1
- update to 0.5.21 (rhbz#990008)

* Fri Jul 26 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-2
- remove one buildrequires: python-sphinx

* Mon Jul 22 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-1
- update to python-pbr-0.5.19 (rhbz#983008)

* Mon Jun 24 2013 Matthias Runge <mrunge@redhat.com> - 0.5.17-1
- update to python-pbr-0.5.17 (rhbz#976026)

* Wed Jun 12 2013 Matthias Runge <mrunge@redhat.com> - 0.5.16-1
- update to 0.5.16 (rhbz#973553)

* Tue Jun 11 2013 Matthias Runge <mrunge@redhat.com> - 0.5.14-1
- update to 0.5.14 (rhbz#971736)

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-2
- remove requirement setuptools_git
- fix docs build under rhel

* Fri May 17 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-1
- update to 0.5.11 (rhbz#962132)
- disable tests, as requirements can not be fulfilled right now

* Thu Apr 25 2013 Matthias Runge <mrunge@redhat.com> - 0.5.8-1
- Initial package.
