Name: fake-qcrilmsgtunnel

Version: 0.3.0
Release: 1
Summary: Fake qcrilmsgtunnel service
License: BSD-3-Clause
URL: https://github.com/sailfishos-sony-nagara/fake-qcrilmsgtunnel
Source: %{name}-%{version}.tar.bz2

BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libglibutil)
BuildRequires: pkgconfig(libgbinder)

Requires(post): systemd
Requires(postun): systemd

%description
%{summary}

%package sim2
Summary: Fake qcrilmsgtunnel service for SIM2
Requires: %{name} = %{version}-%{release}
Requires(post): systemd
Requires(postun): systemd

%description sim2
Fake qcrilmsgtunnel SIM2 service unit.

%prep
%setup -q -n %{name}-%{version}

%build
mkdir build-rpm || true
cd build-rpm
%cmake ..
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
(cd build-rpm && make DESTDIR=%{buildroot} install)

install -d $RPM_BUILD_ROOT%{_unitdir}/graphical.target.wants/
install -m 644 -D %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 644 -D %{name}.service %{buildroot}%{_unitdir}/%{name}-sim2.service
sed -i 's|ExecStart=/usr/sbin/fake-qcrilmsgtunnel|ExecStart=/usr/sbin/fake-qcrilmsgtunnel -s 1|' %{buildroot}%{_unitdir}/%{name}-sim2.service
ln -s ../%{name}.service $RPM_BUILD_ROOT%{_unitdir}/graphical.target.wants/%{name}.service
ln -s ../%{name}-sim2.service $RPM_BUILD_ROOT%{_unitdir}/graphical.target.wants/%{name}-sim2.service

%preun
systemctl daemon-reload || :

%post
systemctl daemon-reload || :

%preun sim2
systemctl daemon-reload || :

%post sim2
systemctl daemon-reload || :

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/graphical.target.wants/%{name}.service

%files sim2
%defattr(-,root,root,-)
%{_unitdir}/%{name}-sim2.service
%{_unitdir}/graphical.target.wants/%{name}-sim2.service
