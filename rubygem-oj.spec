# Generated from oj-2.14.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name oj

# explicitly override gem macros to avoid problems with different
# version and upstream_version
%if 0%{?dlrn} > 0
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{upstream_version}
%global gem_cache   %{gem_dir}/cache/%{gem_name}-%{upstream_version}.gem
%global gem_spec    %{gem_dir}/specifications/%{gem_name}-%{upstream_version}.gemspec
%global gem_docdir  %{gem_dir}/doc/%{gem_name}-%{upstream_version}
%endif

Name:           rubygem-%{gem_name}
Version:        XXX
Release:        1%{?dist}
Summary:        A fast JSON parser and serializer
Group:          Development/Languages
License:        MIT
URL:            http://www.ohler.com/oj
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby-devel
BuildRequires:  rubygem(minitest)

Provides:       rubygem(%{gem_name}) = %{version}

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
%if 0%{?dlrn} > 0
%setup -q -D -T -n  %{dlrn_nvr}
%else
%setup -q -D -T -n  %{gem_name}-%{version}
%endif
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
sed -i "s#require 'minitest'#require 'minitest/unit'#" test/helper.rb


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
%doc %{gem_instdir}/pages/
%doc %{gem_instdir}/README.md
%{gem_instdir}/test


%changelog
