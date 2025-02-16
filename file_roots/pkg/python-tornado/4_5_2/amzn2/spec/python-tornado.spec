%bcond_with python2
%bcond_without python3

%bcond_with tests

%if ( "0%{?dist}" == "0.amzn2" )
%global with_amzn2 1
%endif

%{!?python3_pkgversion:%global python3_pkgversion 3}

%global srcname tornado

Name:           python-%{srcname}
Version:        4.5.2
Release:        5%{?dist}
Summary:        Scalable, non-blocking web server and tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.tornadoweb.org
Source0:        https://files.pythonhosted.org/packages/source/t/tornado/tornado-%{version}.tar.gz
# Patch to use system CA certs instead of certifi
Patch0:         python-tornado-cert.patch

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%if %{with python2}
%package -n python2-%{srcname}
Summary:        Scalable, non-blocking web server and tools
%if 0%{?with_amzn2}
BuildRequires:  python2-rpm-macros
%endif
BuildRequires:  python2-devel
BuildRequires:  python2-backports_abc
BuildRequires:  python2-singledispatch

%{?python_provide:%python_provide python2-%{srcname}}

Requires:       python-pycurl
Requires:       python2-backports_abc
Requires:       python2-singledispatch

%description -n python2-%{srcname}
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package -n python2-doc
Summary:        Examples for python-tornado
Group:          Documentation
Obsoletes:      python2-%{srcname}-doc < 4.2.1-3
Provides:       python2-%{srcname}-doc = %{version}-%{release}

%description -n python2-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.
%endif

%if %{with python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Scalable, non-blocking web server and tools
%if 0%{?with_amzn2}
BuildRequires:  python3-rpm-macros
%endif
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-devel

%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Requires:       python%{python3_pkgversion}-pycurl

%description -n python%{python3_pkgversion}-%{srcname}
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package -n python%{python3_pkgversion}-doc
Summary:        Examples for python-tornado
Group:          Documentation
Obsoletes:      python%{python3_pkgversion}-%{srcname}-doc < 4.2.1-3
Provides:       python%{python3_pkgversion}-%{srcname}-doc = %{version}-%{release}

%description -n python%{python3_pkgversion}-doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%endif # with python3

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1 -b .cert
# remove shebang from files
%{__sed} -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py

%build
%if %{with python3}
## %%py3_build
## amzn2 has an issue with py_setup macro
## py3_shbang_opts is '-s' and causing issues with pip install
## CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" %%{__python3} %%{py_setup} %%{?py_setup_args} build --executable="%%{__p         ython3} %%{py3_shbang_opts}" %%{?*}
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" %{__python3} setup.py %{?py_setup_args} build --executable="%{__python3}" %{?*}
sleep 1

%endif # with python3
%if %{with python2}
%py2_build
%endif


%install
%if %{with python3}
## %%py3_install
## amzn2 has issue with %{py_setup} expansion
cd $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot} %{?*}
%endif # with python3
%if %{with python2}
%py2_install
%endif


%if %{with tests}
%check
%if %{with python3}
%{__python3} -m tornado.test.runtests --verbose
%endif # with python3
%if %{with python2}
%{__python2} -m tornado.test.runtests --verbose
%endif
%endif

%if %{with python2}
%files -n python2-%{srcname}
%doc README.rst
%{python2_sitearch}/%{srcname}/
%{python2_sitearch}/%{srcname}-%{version}-*.egg-info

%files -n python2-doc
%doc demos
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{srcname}
%doc README.rst
%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/%{srcname}-%{version}-*.egg-info

%files -n python%{python3_pkgversion}-doc
%doc demos
%endif


%changelog
* Tue Jan 21 2020 SaltStack Packaging Team <packaging@saltstack.com> - 4.5.2-5
- Updated spec file to not use py3_build  due to '-s' preventing pip installs

* Mon Jan 13 2020 SaltStack Packaging Team <packaging@saltstack.com> - 4.5.2-4
- added definition for python3_pkgversion 3 if not exists

* Mon Jul 01 2019 SaltStack Packaging Team <packaging@saltstack.com> - 4.5.2-3
- Added support for Amazon Linux 2 Python 3, Python 2 support optional

* Tue Nov 07 2017 Charalampos Stratakis <cstratak@redhat.com> - 4.5.2-2
- Fix dist tag and bump release for rebuild

* Tue Nov 07 2017 Charalampos Stratakis <cstratak@redhat.com> - 4.5.2-1
- Update to 4.5.2

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 4.5.1-4
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 20 2017 Orion Poplawski <orion@cora.nwra.com> - 4.5.1-1
- Update to 4.5.1

* Mon Apr 17 2017 Orion Poplawski <orion@cora.nwra.com> - 4.5-1
- Update to 4.5

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 4.4.2-2
- Rebuild for Python 3.6
- Added patch to fix Python 3.6 test failures

* Sun Oct 2 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.2-1
- Update to 4.4.2

* Thu Sep 15 2016 Orion Poplawski <orion@cora.nwra.com> - 4.4.1-1
- Update to 4.4.1
- Drop requires patch, fixed upstream

* Thu Sep 15 2016 Orion Poplawski <orion@cora.nwra.com> - 4.3-5
- Remove backports.ssl_match_hostname from python2-tornado egg requires (bug #1372887)

* Thu Sep 15 2016 Orion Poplawski <orion@cora.nwra.com> - 4.3-4
- Remove certifi from python2-tornado egg requires (bug #1372886)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Feb 22 2016 Orion Poplawski <orion@cora.nwra.com> - 4.3-2
- Properly build python2-tornado

* Thu Feb 18 2016 Orion Poplawski <orion@cora.nwra.com> - 4.3-1
- Update to 4.3
- Drop upstream patches

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-3
- Build python2 packages, drop separate python3 doc package

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 4.2.1-2
- Rebuilt for Python3.5 rebuild
- Add patch to use getfullargspec on python3
- Add patch to fix failing tests with python3.5

* Fri Sep 18 2015 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-1
- Update to 4.2.1
- Modernize spec

* Fri Jul 10 2015 Orion Poplawski <orion@cora.nwra.com> - 4.1-3
- Do not require python-backports-ssl_match_hostname for F22+ (bug #1231368)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 1 2015 Orion Poplawski <orion@cora.nwra.com> - 4.1-1
- Update to 4.1
- Modernize spec

* Fri Dec 5 2014 Orion Poplawski <orion@cora.nwra.com> - 3.2.1-4
- Drop requires python-simplejson

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Thomas Spura <tomspur@fedoraproject.org> - 3.2.1-1
- update to 3.2.1
- no noarch anymore
- remove defattr

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Thomas Spura <tomspur@fedoraproject.org> - 2.2.1-5
- remove rhel conditional for with_python3:
  https://fedorahosted.org/fpc/ticket/200

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.1-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.2.1-1
- update to upstream release 2.2.1 (fixes CVE-2012-2374)
- fix typo for epel6 macro bug #822972 (Florian La Roche)

* Thu Feb 9 2012 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.2-1
- upgrade to upstream release 2.2

* Thu Feb 9 2012 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.1.1-4
- remove python3-simplejson dependency

* Fri Jan 27 2012 Thomas Spura <tomspur@fedoraproject.org> - 2.1.1-3
- build python3 package

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 2.1.1-1
- new upstream version 2.1.1
- remove double word in description and rearrange it (#715272)
- fixed removal of shebangs
- added %%check section to run unittests during package build

* Tue Mar 29 2011 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.2.1-1
- new upstream version 1.2.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep  8 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.1-1
- new upstream release 1.1

* Tue Aug 17 2010 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 1.0.1-1
- new upstream bugfix release: 1.0.1

* Wed Aug  4 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.0-2
- changed upstream source url

* Wed Aug  4 2010 Ionuț C. Arțăriși <mapleoin@fedoraproject.org> - 1.0-1
- new upstream release 1.0
- there's no longer a problem with spurious permissions, so remove that fix

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Oct 21 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.2-3
- changed -doc package group to Documentation
- use global instead of define

* Tue Oct 20 2009 Ionuț Arțăriși <mapleoin@fedoraproject.org> - 0.2-2
- create -doc package for examples
- altered description to not include references to FriendFeed
- rename to python-tornado

* Fri Sep 25 2009 Ionuț Arțăriși <mapleoin@lavabit.com> - 0.2-1
- New upstream version
- Fixed macro usage and directory ownership in spec

* Thu Sep 10 2009 Ionuț Arțăriși <mapleoin@lavabit.com> - 0.1-1
- Initial release

