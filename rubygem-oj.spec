# Generated from oj-2.14.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name oj

Name:           rubygem-%{gem_name}
Version:        2.18.1
Release:        2%{?dist}
Summary:        A fast JSON parser and serializer
Group:          Development/Languages
License:        MIT
URL:            http://www.ohler.com/oj
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0:         0001-Fix-minitest-compatibility.patch

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem(minitest)

Requires:       rubygems

Provides: rubygem(%{gem_name}) = %{version}

%description
The fastest JSON parser and object serializer. .


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%patch0 -p1

# Change ruby interpreter according to packaging guidelines
find . -name \*.rb -type f -print | xargs sed -i 's/#!/usr/bin/env ruby/#!/usr/bin/ruby-mri/'

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%if 0%{?fedora} > 0
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/
%endif

%if 0%{?rhel} >= 7
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
cp -ar .%{gem_instdir}/lib/* %{buildroot}%{gem_extdir_mri}/lib
%endif

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/


# Run the test suite
%check
pushd .%{gem_instdir}/test
ruby -Ilib -Itest -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Tue Oct 24 2017  Martin Mágr <mmagr@redhat.com> - 2.18.1-2
- Fixed SPEC file according to RDO package review (rhbz#1505533)

* Fri Oct 13 2017  Martin Mágr <mmagr@redhat.com> - 2.18.1-1
- Updated to upstream version 2.18.1

* Wed Jun 14 2017 Matthias Runge <mrunge@redhat.com> - 2.14.6-4
- import from https://github.com/opstools-packages/rubygem-oj
- fix provides

* Mon May 09 2016 Martin Mágr <mmagr@redhat.com> - 2.14.6-3
- Explicitly list provides for RHEL

* Mon May 09 2016 Martin Mágr <mmagr@redhat.com> - 2.14.6-2
- Distribute lib files

* Tue May 03 2016 Martin Mágr <mmagr@redhat.com> - 2.14.6-1
- Initial package
