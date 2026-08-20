#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qttasktree
Version:	6.11.2
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qttasktree.git
Source:		qttasktree-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		https://download.qt.io/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qttasktree-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} TaskTree - declarative asynchronous task workflows
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}CorePrivate)
BuildRequires:	cmake(Qt%{major}Concurrent)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	qt%{major}-cmake
License:	GPLv3
# Tech preview in 6.11: library is GPL-3.0-only (no LGPL)

%description
Declarative C++ API for composing and running asynchronous task
workflows (processes, network, threads, timers) with execution
policies and error handling. Tech preview in Qt 6.11.

%define extra_devel_files_TaskTree \
%{_qtdir}/sbom/*

# NO_PRIVATE_MODULE, but the generated CMake config still looks for this
%define extra_devel_reqprov_TaskTree \
Provides: cmake(Qt6TaskTreePrivate) = %{EVRD}

%qt6libs TaskTree

%package examples
Summary:	Examples for the Qt %{major} TaskTree module
Group:		Development/KDE and Qt

%description examples
Examples for the Qt %{major} TaskTree module

%files examples
%{_qtdir}/examples/tasktree

%prep
%autosetup -p1 -n qttasktree%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
