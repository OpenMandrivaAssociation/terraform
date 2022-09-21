#define __debug_package %{nil}
#define _debug_package %{nil}
%define debug_package %{nil}
#define pre rc2

Name:		terraform
Version:	1.3.0
Release:	1
Summary:	Tool for building, changing and versioning infrastructure
License:	MPL-2.0
Group:		Development/Other
Url:		https://www.terraform.io/
# Also: https://www.terraform.io/
Source0:	https://github.com/hashicorp/terraform/archive/refs/tags/v%{version}.tar.gz
# Note latest tarballs from gihub gitea now contain the Go dependencies 
# so the package can be built from source
# Tarball containing go dependencies -- generated by (inside the source tree)
# running:
# export GOPATH=/tmp/.godeps
# go mod download
# cd /tmp
# find .godeps -type d -exec chmod 0755 '{}' +
# find .godeps -type f -exec chmod 0644 '{}' +
# tar cJf godeps-for-terraform-%{version}.tar.xz .godeps
Source1:	godeps-for-terraform-%{version}.tar.xz
BuildRequires:	golang make

%description

%prep
%autosetup -p1
tar xf %{S:1}

%build
export GOPATH="`pwd`/.godeps"
export GOPROXY="file://`pwd`/.godeps"

go build

%install
mkdir -p %{buildroot}%{_bindir}
mv terraform %{buildroot}%{_bindir}

%files
%{_bindir}/terraform
