#define __debug_package %%{nil}
#define _debug_package %%{nil}
%define debug_package %{nil}
#define pre rc2

Name:		terraform
Version:	1.17.1
Release:	1
Summary:	Tool for building, changing and versioning infrastructure
License:	BUSL-1.1
Group:		Development/Other
Url:		https://www.terraform.io/
Source0:	https://github.com/hashicorp/terraform/archive/refs/tags/v%{version}.tar.gz
# GitHub tag archives do not vendor modules. Pack a module cache so the
# ABF build can stay offline (GOPROXY=direct is not enough):
# export GOPATH=/tmp/.godeps
# export GOPROXY=https://proxy.golang.org,direct
# export GOTOOLCHAIN=local
# go mod download
# cd /tmp
# find .godeps -type d -exec chmod 0755 '{}' +
# find .godeps -type f -exec chmod 0644 '{}' +
# tar cJf godeps-for-terraform-%%{version}.tar.xz .godeps
Source1:	godeps-for-terraform-%{version}.tar.xz
BuildRequires:	golang make

%description
Tool for building, changing and versioning infrastructure

%prep
%autosetup -p1
tar xf %{S:1}

%build
export GOPATH="`pwd`/.godeps"
export GOPROXY="file://`pwd`/.godeps"
# go.mod asks for Go 1.26.x; build with the system toolchain and do not
# try to download another one.
export GOTOOLCHAIN=local
# Release builds clear the -dev prerelease marker (see BUILDING.md).
go build -ldflags "-X 'github.com/hashicorp/terraform/version.dev=no'"

%install
mkdir -p %{buildroot}%{_bindir}
mv terraform %{buildroot}%{_bindir}

%files
%license LICENSE
%{_bindir}/terraform
