# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           python-greenlet
Version:        0.3.1
Release:        6%{?dist}
Summary:        Lightweight in-process concurrent programming
Group:          Development/Libraries
License:        MIT
URL:            http://pypi.python.org/pypi/greenlet
Source0:        http://pypi.python.org/packages/source/g/greenlet/greenlet-%{version}.tar.gz

# Based on https://bitbucket.org/ambroff/greenlet/changeset/2d5b17472757
# slightly fixed up to apply cleanly. Avoid rhbz#746771
Patch1:         get-rid-of-ts_origin.patch
# Apply https://bitbucket.org/ambroff/greenlet/changeset/25bf29f4d3b7
# to fix the i686 crash in rhbz#746771
Patch2:         i686-register-fixes.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
The greenlet package is a spin-off of Stackless, a version of CPython
that supports micro-threads called "tasklets". Tasklets run
pseudo-concurrently (typically in a single or a few OS-level threads)
and are synchronized with data exchanges on "channels".

%package devel
Summary:        C development headers for python-greenlet
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains header files required for C modules development.

%prep
%setup -q -n greenlet-%{version}
%patch1 -p1 -b .get-rid-of-ts_origin
%patch2 -p1 -b .i686_register_fixes

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
chmod 644 benchmarks/*.py

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
 
%clean
rm -rf %{buildroot}

# FIXME!!
# The checks segfault on ppc64. So this arch
# is essentially not supported until this is fixed
%ifnarch ppc ppc64
%check
# Run the upstream test suite:
%{__python} setup.py test

# Run the upstream benchmarking suite to further exercise the code:
PYTHONPATH=$(pwd) %{__python} benchmarks/chain.py
PYTHONPATH=$(pwd) %{__python} benchmarks/switch.py
%endif

%files
%defattr(-,root,root,-)
%doc doc/greenlet.txt README benchmarks AUTHORS NEWS
%{python_sitearch}/greenlet.so
%{python_sitearch}/greenlet*.egg-info

%files devel
%defattr(-,root,root,-)
%{_includedir}/python*/greenlet

%changelog
* Mon Oct 24 2011 Pádraig Brady <P@draigBrady.com> - 0.3.1-6
- cherrypick 25bf29f4d3b7 from upstream (rhbz#746771)
- exclude the %check from ppc where the tests segfault

* Wed Oct 19 2011 David Malcolm <dmalcolm@redhat.com> - 0.3.1-5
- add a %%check section
- cherrypick 2d5b17472757 from upstream (rhbz#746771)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 14 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-2
- Splitted headers into a -devel package.

* Fri Apr 09 2010 Lev Shamardin <shamardin@gmail.com> - 0.3.1-1
- Initial package version.
