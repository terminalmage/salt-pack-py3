%bcond_with python2
%bcond_without python3
%bcond_without tests

%{!?python3_pkgversion:%global python3_pkgversion 3}

%if ( "0%{?dist}" == "0.amzn2" )
%global with_amzn2 1
%bcond_with docs
%else
%bcond_without docs
%endif

Name:           python-simplejson

Version:        3.16.0
Release:        3%{?dist}
Summary:        Simple, fast, extensible JSON encoder/decoder for Python

# The main code is licensed MIT.
# The docs include jquery which is licensed MIT or GPLv2
License: (MIT or AFL) and (MIT or GPLv2)
URL:            http://undefined.org/python/#simplejson
Source0:        http://pypi.python.org/packages/source/s/simplejson/simplejson-%{version}.tar.gz
## Source0:        %%pypi_source simplejson


%description
simplejson is a simple, fast, complete, correct and extensible JSON
<http://json.org> encoder and decoder for Python 2.5+. It is pure Python code
with no dependencies, but includes an optional C extension for a serious speed
boost.

The encoder may be subclassed to provide serialization in any kind of
situation, without any special support by the objects to be serialized
(somewhat like pickle).

The decoder can handle incoming JSON strings of any specified encoding (UTF-8
by default).

simplejson is the externally maintained development version of the json library
included with Python 2.6 and Python 3.0, but maintains backwards compatibility
with Python 2.5.  It gets updated more regularly than the json module in the
python stdlib.


%if %{with python2}
%package -n python2-simplejson
Summary:        Simple, fast, extensible JSON encoder/decoder for Python2
BuildRequires:  gcc
BuildRequires:  python2-setuptools
BuildRequires:  python2-nose
%if 0%{?with_amzn2}
BuildRequires:  python2-rpm-macros
BuildRequires:  python-devel
%else
BuildRequires:  python2-devel
%endif
%{?python_provide:%python_provide python2-simplejson}

%description -n python2-simplejson
simplejson is a simple, fast, complete, correct and extensible JSON
<http://json.org> encoder and decoder for Python 2.5+. It is pure Python code
with no dependencies, but includes an optional C extension for a serious speed
boost.

The encoder may be subclassed to provide serialization in any kind of
situation, without any special support by the objects to be serialized
(somewhat like pickle).

The decoder can handle incoming JSON strings of any specified encoding (UTF-8
by default).

simplejson is the externally maintained development version of the json library
included with Python 2.6 and Python 3.0, but maintains backwards compatibility
with Python 2.5.  It gets updated more regularly than the json module in the
python stdlib.
%endif


%if %{with python3}
%package -n python%{python3_pkgversion}-simplejson
Summary:        Simple, fast, extensible JSON encoder/decoder for Python3
BuildRequires: python%{python3_pkgversion}-devel
%if 0%{?with_amzn2}
BuildRequires:  python3-rpm-macros
%endif
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-nose
%if %{with docs}
BuildRequires: python%{python3_pkgversion}-sphinx
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-simplejson}

%description -n python%{python3_pkgversion}-simplejson
simplejson is a simple, fast, complete, correct and extensible JSON
<http://json.org> encoder and decoder for Python 2.5+ and python3.3+ It is pure
Python code with no dependencies, but includes an optional C extension for a
serious speed boost.

The encoder may be subclassed to provide serialization in any kind of
situation, without any special support by the objects to be serialized
(somewhat like pickle).

The decoder can handle incoming JSON strings of any specified encoding (UTF-8
by default).

simplejson is the externally maintained development version of the json library
included with Python 2.6 and Python 3.0, but maintains backwards compatibility
with Python 2.5.  It gets updated more regularly than the json module in the
python stdlib.
%endif


%prep
%setup -q -n simplejson-%{version}

%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
## %%py3_build
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} build --executable="%{__python3} %{py3_shbang_opts}" %{?*}
sleep 1
%endif

%if %{with docs}
PATH=%{_libexecdir}/python%{python3_pkgversion}-sphinx:$PATH %{__python3} scripts/make_docs.py

rm docs/.buildinfo
rm docs/.nojekyll
%endif

%install
%if %{with python2}
%py2_install
%endif
%if %{with python3}
## %%py3_install
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot} %{?*}
%endif

%if %{with tests}
%check
%if %{with python2}
%{__python2} -m nose
%endif
%if %{with python3}
%{__python3} -m nose
%endif
%endif


%if %{with python2}
%files -n python2-simplejson
%license LICENSE.txt
%if %{with docs}
%doc docs
%endif
%{python2_sitearch}/simplejson/
%{python2_sitearch}/simplejson-%{version}-py?.?.egg-info/
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-simplejson
%license LICENSE.txt
%if %{with docs}
%doc docs
%endif
%{python3_sitearch}/simplejson/
%{python3_sitearch}/simplejson-%{version}-py?.?.egg-info/
%endif

%changelog
* Mon Jun 17 2019 SaltStack Packaging Team <packaging@saltstack.com> - 3.16.0-3
- Made support for Python 2 optional

* Wed Oct 03 2018 SaltStack Packaging Team <packaging@saltstack.com> - 3.16.0-2
- Ported to Amazon Linux 2 for Python 3 support

* Thu Aug 23 2018 Miro Hrončok <mhroncok@redhat.com> - 3.16.0-1
- Update to 3.16.0 (#1462583)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  2 2018 Miro Hrončok <mhroncok@redhat.com> - 3.10.0-9
- Use Python 3 Sphinx

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 3.10.0-8
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.10.0-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 3.10.0-2
- Rebuild for Python 3.6

* Fri Nov 4 2016 Orion Poplawski <orion@cora.nwra.com> - 3.10.0-1
- Update to 3.10.0

* Fri Nov 4 2016 Orion Poplawski <orion@cora.nwra.com> - 3.5.3-7
- Enable python 3 support in EPEL
- Ship python2-simplejson
- Modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Luke Macken <lmacken@redhat.com> - 3.5.3-1
- Update to 3.5.3 (#1093685, #1112285)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 07 2014 Luke Macken <lmacken@redhat.com> - 3.4.0-1
- Update to 3.4.0 (#1083979)

* Wed Feb 19 2014 Luke Macken <lmacken@redhat.com> - 3.3.3-1
- Update to 3.3.3 (#960949)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  2 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-1
- Trim changelog to 5 years.
- Update to 3.2.0 upstream feature additions

* Tue Apr  9 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.3-1
- Update to upstream 3.1.3

* Thu Mar 21 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-1
- Update to upstream 3.1.2 (documentation fixes)

* Mon Feb 25 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0 in Rawhide.
- Build the python3 subpackage
- Update to new-style filtering of provides

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0 which changes some messages thrown by exceptions to match
  with json module in python3.3 stdlib.  Probably safe for older releases but
  the python3 version there is 3.2 so there's also not any real need yet.

* Tue May 15 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2
- This update adds new PI but should be backwards compatible

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 9 2011 Toshio Kuratomi <toshoi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0 -- behaviour changing bugfixes

* Mon May 9 2011 Toshio Kuratomi <toshoi@fedoraproject.org> - 2.1.6-1
- Update to 2.1.6 for a segfault fix

* Sat Apr 30 2011 Toshio Kuratomi <toshoi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5, trivial upstream release (change makes more compact output)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Toshio Kuratomi <toshoi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Mon Dec 20 2010 Toshio Kuratomi <toshoi@fedoraproject.org> - 2.1.2-1
- Update to upstream 2.1.2, a bugfix release with four small, self-contained
  fixes.

* Wed Oct 20 2010 Toshio Kuratomi <toshoi@fedoraproject.org> - 2.1.1-4
- Simplify the %%files section to own the tests directory
- Use the fedora documented filter functions to filter provides

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 30 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2.1.1-2
- Filter unnecessary provides
- License tag update
- Minor spec file cleanups

* Mon Jun 21 2010 Kyle VanderBeek <kylev@kylev.com> - 2.1.1-1
- Update to 2.1.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Kyle VanderBeek <kylev@kylev.com> - 2.0.9-2
- Remove ill-advised gcc BuildRequires

* Thu Jun  4 2009 Kyle VanderBeek <kylev@kylev.com> - 2.0.9-1
- Update to 2.0.9
- Make sure to require gcc to the speedups get compiled
- Fix description since we're not "pure" python
- Change to pypi instead of cheesehop

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> 2.0.7-1
- Update to 2.0.7

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.3-3
- Rebuild for Python 2.6

* Thu Oct 23 2008 Luke Macken <lmacken@redhat.com> 2.0.3-2
- Use nose to run the simplejson test suite

* Mon Oct 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.3-1
- update to 2.0.3

* Wed Oct 01 2008 Luke Macken <lmacken@redhat.com> - 2.0.1-1
- Update to 2.0.1, which contains many optimizations and bugfixes

* Wed Sep 24 2008 Luke Macken <lmacken@redhat.com> - 1.9.3-1
- Update to 1.9.3, which includes a significant decoding speed boost, and
  various bug fixes.

* Tue May 06 2008 Luke Macken <lmacken@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Wed Apr 02 2008 Luke Macken <lmacken@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Thu Feb 28 2008 Luke Macken <lmacken@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Fri Feb  8 2008 Luke Macken <lmacken@redhat.com> - 1.7.3-3
- Rebuild for gcc 4.3
