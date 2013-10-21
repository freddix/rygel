Summary:	Home media solution (UPnP AV MediaServer)
Name:		rygel
Version:	0.20.1
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/rygel/0.20/%{name}-%{version}.tar.xz
# Source0-md5:	1621cd63519c8bf9cccd8a1a51d982fd
URL:		https://live.gnome.org/Rygel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gssdp-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk+3-devel >= 3.10.0
BuildRequires:	gupnp-av-devel
BuildRequires:	gupnp-dlna-devel >= 0.9.4
BuildRequires:	intltool
BuildRequires:	libgee-devel
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
BuildRequires:	sqlite3-devel
BuildRequires:	tracker-devel
BuildRequires:	vala
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus
Requires:	gstreamer-plugins-base
Requires:	shared-mime-info
Suggests:	gstreamer-libav
Suggests:	gstreamer-plugins-bad
Suggests:	gstreamer-plugins-good
Suggests:	gstreamer-plugins-ugly
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rygel is a home media solution that allows you to easily share audio,
video and pictures, and control of media player on your home network.
In technical terms it is both a UPnP AV MediaServer and MediaRenderer
implemented through a plug-in mechanism. Interoperability with other
devices in the market is achieved by conformance to very strict
requirements of DLNA and on the fly conversion of media to format that
client devices are capable of handling.

%package libs
Summary:	Rygel libraries
Group:		Libraries

%description libs
Shared Rygel libraries.

%package devel
Summary:	Header files for Rygel libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This is the package containing the header files for Rygel libraries.

%package plugin-tracker
Summary:	Rygel plugins
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	tracker

%description plugin-tracker
Media export plugin using Tracker

%package apidocs
Summary:	API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Rygel libraries API documentation.

%prep
%setup -q

# hardcoded gtk-doc dir
%{__sed} -i "s|gtk-doc/html|doc/gtk-doc/html|" doc/reference/doc-build.am

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules		\
	--enable-gst-launch-plugin	\
	--enable-mediathek-plugin
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -name *.la -exec rm {} \;

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rygel.conf
%attr(755,root,root) %{_bindir}/rygel
%attr(755,root,root) %{_bindir}/rygel-preferences

%dir %{_libdir}/rygel-2.0
%dir %{_libdir}/rygel-2.0/engines
%attr(755,root,root) %{_libdir}/rygel-2.0/engines/librygel-media-engine-gst.so
%attr(755,root,root) %{_libdir}/rygel-2.0/engines/librygel-media-engine-simple.so
%{_libdir}/rygel-2.0/engines/*.plugin

%dir %{_libdir}/rygel-2.0/plugins
%attr(755,root,root) %{_libdir}/rygel-2.0/plugins/librygel-external.so
%attr(755,root,root) %{_libdir}/rygel-2.0/plugins/librygel-gst-launch.so
%attr(755,root,root) %{_libdir}/rygel-2.0/plugins/librygel-media-export.so
%attr(755,root,root) %{_libdir}/rygel-2.0/plugins/librygel-mediathek.so
%attr(755,root,root) %{_libdir}/rygel-2.0/plugins/librygel-mpris.so
%attr(755,root,root) %{_libdir}/rygel-2.0/plugins/librygel-playbin.so
%{_libdir}/rygel-2.0/plugins/*.plugin

%{_datadir}/dbus-1/services/org.gnome.Rygel1.service
%{_datadir}/rygel
%{_desktopdir}/rygel-preferences.desktop
%{_desktopdir}/rygel.desktop
%{_iconsdir}/hicolor/*/apps/rygel*.*
%{_mandir}/man1/rygel.1*
%{_mandir}/man5/rygel.conf.5*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/librygel-core-2.0.so.1
%attr(755,root,root) %ghost %{_libdir}/librygel-server-2.0.so.1
%attr(755,root,root) %ghost %{_libdir}/librygel-renderer-2.0.so.1
%attr(755,root,root) %ghost %{_libdir}/librygel-renderer-gst-2.0.so.1
%attr(755,root,root) %{_libdir}/librygel-core-2.0.so.*.*.*
%attr(755,root,root) %{_libdir}/librygel-renderer-2.0.so.*.*.*
%attr(755,root,root) %{_libdir}/librygel-renderer-gst-2.0.so.*.*.*
%attr(755,root,root) %{_libdir}/librygel-server-2.0.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librygel-core-2.0.so
%attr(755,root,root) %{_libdir}/librygel-renderer-2.0.so
%attr(755,root,root) %{_libdir}/librygel-renderer-gst-2.0.so
%attr(755,root,root) %{_libdir}/librygel-server-2.0.so
%{_includedir}/rygel-2.0
%{_pkgconfigdir}/*.pc
%{_datadir}/vala/vapi/*.deps
%{_datadir}/vala/vapi/*.vapi

%files plugin-tracker
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/rygel-2.0/plugins/librygel-tracker.so

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/librygel-*

