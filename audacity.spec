# TODO:
#       it constantly tries to open /usr/bin/Portable Settings/*
#       internal portaudio crashes when only OSS is available on startup
#	use system nyquist?
#	Installed (but unpackaged) file(s) found:
#	   /usr/share/doc/audacity/LICENSE.txt
#	   /usr/share/doc/audacity/README.txt
Summary:	Audacity - manipulate digital audio waveforms
Summary(pl):	Audacity - narz�dzie do obr�bki plik�w d�wi�kowych
Summary(ru):	������������������ �������� ��������
Name:		audacity
Version:	1.3.2
Release:	2
License:	GPL
Vendor:		Dominic Mazzoni <dominic@minorninth.com>
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/audacity/%{name}-src-%{version}.tar.gz
# Source0-md5:	bf63673140254f1283dfd55b61ff2422
Source1:	%{name}.desktop
Source2:	%{name}-icon.png
Patch0:		%{name}-not_require_lame-libs-devel.patch
Patch1:		%{name}-wx28.patch
Patch2:		%{name}-flac.patch
Patch3:		%{name}-system-libs.patch
Patch4:		%{name}-opt.patch
URL:		http://audacity.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	expat-devel >= 1.95
BuildRequires:	fftw-devel >= 2.1.4
BuildRequires:	flac-devel >= 1.1.3
BuildRequires:	gettext-devel
BuildRequires:	libid3tag-devel >= 0.15.0b-2
BuildRequires:	libjpeg-devel
BuildRequires:	libmad-devel >= 0.14.2b-4
BuildRequires:	libresample-devel >= 0.1.3
BuildRequires:	libsamplerate-devel >= 0.1.2
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	pkgconfig
BuildRequires:	soundtouch-devel >= 1.3.0
BuildRequires:	speex-devel
BuildRequires:	which
BuildRequires:	wxGTK2-unicode-devel >= 2.8.0
BuildRequires:	zip
Requires:	lame-libs
Requires:	libid3tag >= 0.15.0b-2
Requires(post,postun):	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Audacity is a program that lets you manipulate digital audio
waveforms. It imports many sound file formats, including WAV, AIFF,
AU, IRCAM, MP3, and Ogg Vorbis. It supports all common editing
operations such as Cut, Copy, and Paste, plus it will mix tracks and
let you apply plug-in effects to any part of a sound.

%description -l pl
Audacity to program obs�uguj�cy r�ne formaty plik�w audio. Obs�uguje
WAV, AIFF, AU, IRCAM, MP3, oraz Ogg Vorbis. Program ten umo�liwia
wykonywanie podstawowych czynno�ci edycyjnych takich jak kasowanie,
wstawianie i miksowanie �cie�ki d�wi�kowej. Umo�liwia tak�e
wykonywanie dowolnych innych operacji poprzez system wtyczek.

%description -l ru
Audacity - ��� �������� ��������, ����������� �������� � ������� �
�������� WAV, AIFF, AU, IRCAM, MP3 � Ogg Vorbis. � ��� ����������� ���
�������� ��������, ����� ��� ��������, �����������, �������,
������������ ������ � ���������� ��������, ����������� � ����
��������, � ����� ����� ��������� �����.

%prep
%setup -q -n %{name}-src-%{version}-beta
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
cd lib-src/portmixer
%{__autoconf}
cd ../..
%{__aclocal}
%{__autoconf}

export WX_CONFIG="`which wx-gtk2-unicode-config`"
%configure \
	--with-help \
	--with-id3tag=system \
	--with-libmad=system \
	--with-libsamplerate=system \
	--with-libsndfile=system \
	--with-libflac=system \
	--with-vorbis=system

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_PATH=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{zh,zh_CN}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database

%postun
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/audacity
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_datadir}/mime/packages/audacity.xml
