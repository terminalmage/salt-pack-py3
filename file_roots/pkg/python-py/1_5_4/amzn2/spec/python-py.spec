%bcond_with python2
%bcond_without python3

%{!?python3_pkgversion:%global python3_pkgversion 3}

%if ( "0%{?dist}" == "0.amzn2" )
%global with_amzn2 1
%bcond_with docs
%bcond_with tests
%else

# we have a circular (build) dependency with the (new) pytest package
# when generating the docs or running the testsuite
%bcond_without docs
# the testsuite is curremtly not compatible with pytest 3, see
# https://github.com/pytest-dev/py/issues/104
%if 0%{?fedora} >= 26 || 0%{?rhel} > 7
%bcond_with tests
%else
%bcond_without tests
%endif
%endif

%global pytest_version_lb 2.9.0
%global pytest_version_ub 2.10

%global srcname py

Name:           python-%{srcname}
Version:        1.5.4
Release:        5%{?dist}
Summary:        Library with cross-python path, ini-parsing, io, code, log facilities
License:        MIT and Public Domain
#               main package: MIT, except: doc/style.css: Public Domain
URL:            http://pylib.readthedocs.io/en/stable/
Source:         https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%if %{with tests}
# needed by the testsuite
BuildRequires:  subversion
%endif # with tests

%description
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects


%if %{with python2}
%package -n python2-%{srcname}
Summary:        Library with cross-python path, ini-parsing, io, code, log facilities
%if 0%{?with_amzn2}
BuildRequires:  python2-rpm-macros
BuildRequires:  python-devel
%else
BuildRequires:  python2-devel
%endif
BuildRequires:  python2-setuptools
BuildRequires:  python2-setuptools_scm
%if %{with docs}
BuildRequires:  %{_bindir}/sphinx-build-2
%endif # with_docs
%if %{with tests}
BuildRequires:  python2-pytest >= %{pytest_version_lb}, python2-pytest < %{pytest_version_ub}
%endif # with tests
Requires:       python2-setuptools
%{?python_provide:%python_provide python2-%{srcname}}
Provides:       bundled(python2-apipkg) = 1.4
Provides:       bundled(python2-iniconfig) = 1.0.0

%description -n python2-%{srcname}
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects

%endif # with python2


%if %{with python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Library with cross-python path, ini-parsing, io, code, log facilities
%if 0%{?with_amzn2}
BuildRequires:  python3-rpm-macros
%endif
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools_scm
%if %{with docs}
BuildRequires:  %{_bindir}/sphinx-build-3
%endif # with_docs
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest >= %{pytest_version_lb}, python%{python3_pkgversion}-pytest < %{pytest_version_ub}
%endif # with tests
Requires:       python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python3-%{srcname}}
Provides:       bundled(python3-apipkg) = 1.4
Provides:       bundled(python3-iniconfig) = 1.0.0
Obsoletes:      platform-python-%{srcname} < %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects

%endif # with python3


%prep
%setup -qc -n %{srcname}-%{version}

# remove shebangs and fix permissions
find %{srcname}-%{version} \
   -type f -a \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;

%if %{with python2}
mv %{srcname}-%{version} python2
%endif
%if %{with python3}
mv %{srcname}-%{version} python3
%endif


%build
%if %{with python2}
pushd python2
%py2_build
%if %{with docs}
make -C doc html PYTHONPATH=$(pwd) SPHINXBUILD=sphinx-build-2
%endif # with docs
popd
%endif # with python2

%if %{with python3}
pushd python3
## %%py3_build
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} build --executable="%{__python3} %{py3_shbang_opts}" %{?*}
sleep 1
%if %{with docs}
make -C doc html PYTHONPATH=$(pwd) SPHINXBUILD=sphinx-build-3
%endif # with docs
popd
%endif # with python3


%install
%if %{with python2}
pushd python2
%py2_install
# remove hidden file
rm -rf doc/_build/html/.buildinfo
popd
%endif # with python2

%if %{with python3}
pushd python3
## %%py3_install
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot} %{?*}
# remove hidden file
rm -rf doc/_build/html/.buildinfo
popd
%endif # with python3


%check
%if %{with tests}
# disable failing Subversion checks for now

%if %{with python2}
pushd python2
PYTHONPATH=%{buildroot}%{python2_sitelib} \
LC_ALL="en_US.UTF-8" \
py.test-%{python2_version} -r s -k"-TestWCSvnCommandPath" testing
popd
%endif # with python2

%if %{with python3}
pushd python3
PYTHONPATH=%{buildroot}%{python3_sitelib} \
LC_ALL="en_US.UTF-8" \
py.test-%{python3_version} -r s -k"-TestWCSvnCommandPath" testing
popd
%endif # with python3

%endif # with tests


%if %{with python2}
%files -n python2-%{srcname}
%doc python2/CHANGELOG
%doc python2/README.rst
%license python2/LICENSE
%if %{with docs}
%doc python2/doc/_build/html
%endif # with_docs
%{python2_sitelib}/py-*.egg-info/
%{python2_sitelib}/py/
%endif # with python2


%if %{with python3}
%files -n python%{python3_pkgversion}-%{srcname}
%doc python3/CHANGELOG
%doc python3/README.rst
%license python3/LICENSE
%if %{with docs}
%doc python3/doc/_build/html
%endif # with_docs
%{python3_sitelib}/py-*.egg-info/
%{python3_sitelib}/py/
%endif # with python3


%changelog
* Mon Jun 17 2019 SaltStack Packaging Team <packaging@saltstack.com> - 1.5.4-5
- Made support for Python 2 optional

* Wed Oct 10 2018 SaltStack Packaging Team <packaging@saltstack.com> - 1.5.4-4
- Support for Python 3 on Amazon Linux 2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.4-2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.4-1
- Update to 1.5.4.
- Add BR on setuptools_scm.

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.3-3
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.3-2
- Bootstrap for Python 3.7

* Thu Mar 22 2018 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.3-1
- Update to 1.5.3.

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.5.2-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.2-1
- Update to 1.5.2.

* Wed Nov 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.1-1
- Update to 1.5.1.
- Update list of vendored packages.
- Fix HTML doc path.

* Wed Nov 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.34-8
- Restore earlier structure of the spec file, also fixing previously
  introduced problems.

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.34-7
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.34-6
- Remove platform-python subpackage

* Tue Sep 05 2017 Troy Dawson <tdawson@redhat.com> - 1.4.34-5
- Cleanup spec file conditionals

* Fri Aug 11 2017 Tomas Orsava <torsava@redhat.com> - 1.4.34-4
- Switch with_docs and run_test macros to bcond_without docs, tests

* Thu Aug 10 2017 Tomas Orsava <torsava@redhat.com> - 1.4.34-3
- Added the platform-python subpackage

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun  5 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.34-1
- Update to 1.4.34.

* Sun Mar 19 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.33-1
- Update to 1.4.33.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.32-2
- Enable tests for Fedora<26.

* Thu Dec 29 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.32-1
- Update to 1.4.32.

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.4.31-5
- Rebuild for Python 3.6
- Disable tests

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.31-2
- Re-enable checks and docs.

* Sat Jan 23 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.31-1
- Update to 1.4.31.
- Follow updated Python packaging guidelines.
- Add Provides tag for bundled apipkg.

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 1.4.30-3
- Rebuilt for Python3.5 rebuild
- With check and docs

* Wed Sep 23 2015 Robert Kuska <rkuska@redhat.com> - 1.4.30-2
- Rebuilt for Python3.5 rebuild without check and docs

* Mon Jul 27 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.30-1
- Update to 1.4.30.

* Thu Jun 25 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.29-1
- Update to 1.4.29.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.28-1
- Update to 1.4.28.
- Modernize spec file.
- Apply updates Python packaging guidelines.
- Mark LICENSE with %%license.

* Sat Dec  6 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.26-2
- Re-enable doc building and testsuite.

* Tue Dec  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.26-1
- Update to 1.4.26.

* Sat Oct 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.25-2
- Re-enable doc building and testsuite.

* Sat Oct 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.25-1
- Update to 1.4.25.

* Wed Aug  6 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.23-1
- Update to 1.4.23.

* Fri Aug  1 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.22-2
- Re-enable doc building and testsuite.

* Fri Aug  1 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.22-1
- Update to 1.4.22.

* Fri Jul 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.21-1
- Update to 1.4.21.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.20-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 1.4.20-2.1
- rebuild for python 3.4 disable tests for circular deps

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.20-2
- Re-enable doc building and testsuite.

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.20-1
- Update to 1.4.20.

* Sun Nov 10 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.18-1
- Update to 1.4.18.

* Mon Oct  7 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.17-2
- Only run tests from the 'testing' subdir in %%check.

* Fri Oct  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.17-1
- Update to 1.4.17.

* Thu Oct  3 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.16-1
- Update to 1.4.16.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 30 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.15-1
- Update to 1.4.15.
- Disable failing Subversion checks for now.

* Wed Jun 12 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.14-2
- Use python-sphinx for rhel > 6 (rhbz#973321).
- Update URL.
- Fix changelog entry with an incorrect date (rhbz#973325).

* Sat May 11 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.14-1
- Update to 1.4.14.

* Sat Mar  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.13-1
- Update to 1.4.13.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.12-1
- Update to 1.4.12.

* Sat Oct 27 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.11-1
- Update to 1.4.11.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.10-2
- Re-enable doc building and testsuite.
- Minor testsuite fixes.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.10-1
- Update to 1.4.10.

* Fri Oct 12 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-8
- Re-enable doc building and testsuite.

* Thu Oct 11 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-7
- Add conditional for sphinx on rhel.
- Remove rhel logic from with_python3 conditional.

* Wed Oct 10 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-6
- Re-enable doc building and testsuite.

* Sat Aug  4 2012 David Malcolm <dmalcolm@redhat.com> - 1.4.9-5
- Temporarily disable docs and testsuite.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.4.9-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-2
- Re-enable doc building and testsuite.

* Thu Jun 14 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-1
- Update to 1.4.9.

* Sat Jun  9 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.8-2
- Re-enable doc building and testsuite.

* Wed Jun  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.8-1
- Update to 1.4.8.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.7-2
- Re-enable doc building and testsuite.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.7-1
- Update to 1.4.7.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.6-2
- Re-enable doc building and testsuite.

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.6-1
- Update to 1.4.6.
- Remove %%prerelease macro.
- Temporarily disable docs and testsuite.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-4
- Rebuilt for glibc bug#747377

* Sat Sep  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.5-3
- Fix: python3 dependencies.

* Tue Aug 30 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.5-2
- Re-enable doc building and testsuite.

* Sat Aug 27 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.5-1
- Update to 1.4.5.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.4-2
- Re-enable doc building and testsuite.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.4-1
- Update to 1.4.4.
- Upstream provides a .zip archive only.
- pytest and pycmd are separate packages now.
- Disable building html docs und the testsuite to break the circular
  build dependency with pytest.
- Update summary and description.
- Remove BRs no longer needed.
- Create a Python 3 subpackage.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 18 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.4-1
- Update to 1.3.4

* Fri Aug 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.3-2
- Add dependency on python-setuptools (see bz 626808).

* Sat Jul 31 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.3-1
- Update to 1.3.3.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 10 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.2-1
- Update to 1.3.2.
- Do cleanups already in %%prep to avoid inconsistent mtimes between
  source files and bytecode.

* Sat May 29 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.1-1
- Update to 1.3.1.

* Sat May  8 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.0-1
- Update to 1.3.0.
- Remove some backup (.orig) files.

* Sun Feb 14 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.1-1
- Update to 1.2.1.

* Wed Jan 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.0-1
- Update to 1.2.0.
- Adjust summary and %%description.
- Use %%global instead of %%define.

* Sat Nov 28 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-1
- Update to 1.1.1.

* Sat Nov 21 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-1
- Update to 1.1.0. Upstream reorganized the package's structure and
  cleaned up the install process, so the specfile could be greatly
  simplified.
- Dropped licenses for files no longer present from the License tag.

* Thu Aug 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.2-1
- Update to 1.0.2.
- One failing test is no longer part of the testsuite, thus needs not
  to be skipped anymore.
- Some developer docs are missing this time in upstream's tarfile, so
  cannot be moved to %%{_docdir}

* Thu Aug 13 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-1
- Update to 1.0.0.
- Re-enable SVN tests in %%check.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-1.b8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-0.b8
- Update to 1.0.0b8.
- Remove patches applied upstream.
- Greenlets have been removed upstream. So, package is noarch and
  - installs to %%{python_sitelib} again
  - %%ifarch sections have been removed.
- Don't remove files used by the testsuite for now.
- Add dependency on python-pygments, pylint and pexpect (for the
  testsuite).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-6
- Use system doctest module again, as this wasn't the real cause of
  the test failure. Instead, remove the failing test for now.

* Fri Dec 12 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-5
- Add patch from trunk fixing a subversion 1.5 problem (pylib
  issue66).
- Don't replace doctest compat module (pylib issue67).

* Fri Nov 21 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-4
- Use dummy_greenlet on ppc and ppc64.

* Tue Oct  7 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-3
- Replace compat modules by stubs using the system modules instead.
- Add patch from trunk fixing a timing issue in the tests.

* Tue Sep 30 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-2
- Update license information.
- Fix the tests.

* Sun Sep  7 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-1
- Update to 0.9.2.
- Upstream now uses setuptools and installs to %%{python_sitearch}.
- Remove %%{srcname} macro.
- More detailed information about licenses.

* Thu Aug 21 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.1-1
- New package.
