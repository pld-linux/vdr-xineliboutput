#
%define		plugin_name	xineliboutput
Summary:	X11 and framebuffer front-end for VDR
Name:		vdr-%{plugin_name}
Version:	1.0.7
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://netcologne.dl.sourceforge.net/project/xineliboutput/xineliboutput/vdr-xineliboutput-1.0.7/%{name}-%{version}.tar.lzma
# Source0-md5:	55bc903eb5181806ed71a9d11333e73f
URL:		http://sourceforge.net/projects/xineliboutput/
BuildRequires:	dbus-glib-devel
BuildRequires:	libextractor-devel >= 0.5.20
BuildRequires:	libjpeg-devel
BuildRequires:	vdr-devel >= 1.4.0
BuildRequires:	xine-lib-devel >= 1.1.1
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# plugins use symbols provided by the binary
%define		skip_post_check_so	.*%{_libdir}/vdr/lib.*-.*\.so\..*

%description
VDR plugin for xine-lib based software output device.
* Supports X11 and Linux framebuffer
* Connects to VDR locally or over network
* Built-in media player

%prep
%setup -q -n %{plugin_name}-%{version}
%{__sed} -e 's/\(#if VDRVERSNUM >\) 10700/\1 10800/' -i xineliboutput.c
%{__sed} -e 's/\(OBJS_FBFE) $(LIBS_XINE) -ljpeg\)/\1 -lpthread/' -i Makefile
%{__mkdir} -p lib locale

%build
# OPTFLAGS is used partially
%{__make} \
	CFLAGS="%{rpmcflags} -fPIC" \
	CXXFLAGS="%{rpmcflags} -fPIC -Woverloaded-virtual" \
	VDRDIR=%{_includedir}/vdr \
	LIBDIR=lib \
	LOCALEDIR=locale

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/vdr,%{_localedir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LOCALEDIR=$RPM_BUILD_ROOT%{_localedir}

cp lib/lib*.so.* $RPM_BUILD_ROOT%{_libdir}/vdr

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc HISTORY README
%attr(755,root,root) %{_bindir}/vdr-*fe
%attr(755,root,root) %{_libdir}/vdr/libvdr-xineliboutput.so.*
%attr(755,root,root) %{_libdir}/vdr/libxineliboutput-*fe.so.*
%attr(755,root,root) %{_libdir}/xine/plugins/*/xineplug_inp_xvdr.so
%attr(755,root,root) %{_libdir}/xine/plugins/*/post/xineplug_post_*.so
