Name:       ibus
Version:    1.5.4
Release:    0
Summary:    Intelligent Input Bus for Linux OS
License:    LGPL-2.0+
Group:      System/Libraries
URL:        http://code.google.com/p/ibus/
Source0:    http://ibus.googlecode.com/files/%{name}-%{version}.tar.gz
Source1001: ibus.manifest

BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  dbus-glib-devel
BuildRequires:  dbus-python-devel
BuildRequires:  python-devel
BuildRequires:  intltool
BuildRequires:  iso-codes-devel
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pygobject-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala

Requires:   %{name}-libs = %{version}-%{release}

Requires:   pygobject
Requires:   iso-codes
Requires:   dbus-python

%description
IBus is an input framework for Linux OS.

%package libs
Summary:    IBus libraries
Group:      System/Libraries

Requires:   dbus >= 1.2.4

%description libs
This package contains the libraries for IBus

%package devel
Summary:    Development tools for IBus
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}
Requires:   glib2-devel
Requires:   dbus-devel

%description devel
The ibus-devel package contains the header files for IBus

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --disable-static \
           --disable-tests \
           --disable-gtk2 \
           --disable-gtk3 \
           --disable-xim \
           --enable-wayland \
           --disable-vala \
           --disable-gtk-doc \
           --disable-gconf \
           --disable-setup \
           --disable-dconf \
           --enable-python-library \
           --disable-ui \
           --disable-libnotify \
           --enable-introspection

%__make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/libibus-1.0.la

rm -fr %{buildroot}%{_datadir}/gtk-doc

%find_lang %{name}10

%clean
rm -rf %{buildroot}

%post
# recreate icon cache
touch --no-create %{_datadir}/icons/hicolor || :
[ -x %{_bindir}/gtk-update-icon-cache ] && \
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%posttrans
# create registry cache
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%postun
# recreate icon cache
touch --no-create %{_datadir}/icons/hicolor || :
[ -x %{_bindir}/gtk-update-icon-cache ] && \
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
# 'ibus write-cache --system' updates the system cache.
[ -f /var/cache/ibus/bus/registry ] && \
  rm /var/cache/ibus/bus/registry || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files -f %{name}10.lang
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{python_sitelib}/ibus
%{python_sitelib}/ibus/*
%dir %{_datadir}/ibus/
%{_bindir}/ibus
%{_bindir}/ibus-daemon
%{_datadir}/ibus/keymaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_libexecdir}/*
%{_datadir}/ibus/component/simple.xml
%{_datadir}/bash-completion/completions/ibus.bash
%{_datadir}/man/man1/*

%files libs
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libibus-1.0.so.*
%{_libdir}/girepository-1.0/IBus-1.0.typelib

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/IBus-1.0.gir
