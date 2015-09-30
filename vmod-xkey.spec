Summary: Surrogate keys support for Varnish Cache
Name: vmod-xkey
Version: 1.0
Release: 1%{?dist}
License: BSD
Group: System Environment/Daemons
Source0: libvmod-xkey-trunk.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: varnish >= 4.0.2
BuildRequires: make
BuildRequires: python-docutils
BuildRequires: varnish >= 4.0.2
BuildRequires: varnish-libs-devel >= 4.0.2

%description
Surrogate keys support for Varnish Cache.

%prep
%setup -n libvmod-xkey-trunk

%build
%configure --prefix=/usr/
%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} check

%install
[ %{buildroot} != "/" ] && %{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%clean
[ %{buildroot} != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/varnis*/vmods/
%doc /usr/share/doc/lib%{name}/*
%{_mandir}/man?/*

%changelog
* Wed Sep 30 2015 Martin Blix Grydeland <martin@varnish-software.com> - 0.1-0.20150930
- Initial version.
