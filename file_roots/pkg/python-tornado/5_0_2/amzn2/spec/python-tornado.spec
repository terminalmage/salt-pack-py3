%bcond_with python2
%bcond_without python3
%bcond_with tests

%{!?python3_pkgversion:%global python3_pkgversion 3}

%if ( "0%{?dist}" == "0.amzn2" )
%global with_amzn2 1
%endif

%global srcname tornado

Name:           python-%{srcname}
Version:        5.0.2
Release:        6%{?dist}
Summary:        Scalable, non-blocking web server and tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.tornadoweb.org
Source0:        https://files.pythonhosted.org/packages/source/t/tornado/tornado-%{version}.tar.gz

# If unittest2 instead of unittest is used while running the tests,
# the deprecation warnings will make the test suite error out.
# Fixed upstream: https://github.com/tornadoweb/tornado/pull/2350/commits/1a9b9939376b80d9f053734f539b860e0dca1aff
Patch0:         fix-erroneous-deprecation-warnings.patch

BuildRequires:  gcc


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
BuildRequires:  python-devel
BuildRequires:  python-singledispatch
%else
BuildRequires:  python2-devel
BuildRequires:  python2-singledispatch
%endif
BuildRequires:  python2-backports_abc
BuildRequires:  python2-futures
%{?python_provide:%python_provide python2-%{srcname}}

%if 0%{?with_amzn2}
Requires:       python-pycurl
Requires:       python-backports_abc
Requires:       python-singledispatch
%else
Requires:       python2-pycurl
Requires:       python2-backports_abc
Requires:       python2-singledispatch
%endif
Requires:       python2-futures

%description -n python2-%{srcname}
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.
%endif  # with python2

%if %{with python3}
%package doc
Summary:        Examples for python-tornado
Group:          Documentation
Obsoletes:      python%{python3_pkgversion}-%{srcname}-doc < 4.2.1-3
Provides:       python%{python3_pkgversion}-%{srcname}-doc = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Scalable, non-blocking web server and tools
%if 0%{?with_amzn2}
BuildRequires:  python3-rpm-macros
%endif
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
Requires:       python%{python3_pkgversion}-pycurl
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.
%endif

%prep 
## %%setup -q -n %%{srcname}-%%{version}
%setup -n %{srcname}-%{version}
%patch0 -p1
# remove shebang from files
%{__sed} -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py

%build
%if %{with python3}
## %%py3_build
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} build --executable="%{__python3} %{py3_shbang_opts}" %{?*}
sleep 1
%endif
%if %{with python2}
%py2_build
%endif


%install
%if %{with python3}
## %%py3_install
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot} %{?*}
%endif
%if %{with python2}
%py2_install
%endif

%if %{with tests}
%check
%if %{with python3}
%{__python3} -m tornado.test.runtests --verbose
%endif
%if %{with python2}
%{__python2} -m tornado.test.runtests --verbose
%endif

%if %{with python2}
%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitearch}/%{srcname}/
%{python2_sitearch}/%{srcname}-%{version}-*.egg-info
%endif # with python2

%files doc
%doc demos
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{srcname}/
%{python3_sitearch}/%{srcname}-%{version}-*.egg-info
%endif


%changelog
* Mon Jun 17 2019 SaltStack Packaging Team <packaging@saltstack.com> - 5.0.2-6
- Made support for Python 2 optional

* Thu Oct 04 2018 SaltStack Packaging Team <packaging@saltstack.com> - 5.0.2-5
- Ported to Amazon Linux 2 for Python 3 support

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 5.0.2-3
- Rebuilt for Python 3.7

* Sat May 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.0.2-2
- Require python2-futures

* Fri May 18 2018 Charalampos Stratakis <cstratak@redhat.com> - 5.0.2-1
- Update to 5.0.2

* Thu Apr 26 2018 Lumír Balhar <lbalhar@redhat.com> - 4.5.2-5
- New conditionals for Python 2
- Drop Python 3 conditional

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.5.2-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

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

