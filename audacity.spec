#
# Conditional build:
# _with_gtk1	- use wxGTK instead of wxGTK2
#
Summary:	Audacity - manipulate digital audio waveforms
Summary(pl):	Audacity - narz�dzie do obr�bki plik�w d�wi�kowych
Summary(ru):	������������������ �������� ��������
Name:		audacity
Version:	1.1.3
Release:	1
License:	GPL
Vendor:		Dominic Mazzoni <dominic@minorninth.com>
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/%{name}/%{name}-src-%{version}.tgz
Source1:	%{name}.desktop
Source2:	%{name}-icon.png
Patch0:		%{name}-system-expat.patch
Patch1:		%{name}-helpfile_location.patch
Patch2:		%{name}-not_require_lame-libs-devel.patch
Patch3:		%{name}-opt.patch
URL:		http://audacity.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	expat-devel
BuildRequires:	fftw-devel >= 2.1.4
BuildRequires:	flac-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	mad-devel >= 0.14.2b-4
%{?_with_gtk1:BuildRequires:	wxGTK-devel >= 2.4.0}
%{!?_with_gtk1:BuildRequires:	wxGTK2-devel >= 2.4.0}
Requires:	lame-libs
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
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__autoconf}
export WX_CONFIG="`which wxgtk%{!?_with_gtk1:2}-2.4-config`"
%configure \
	--with-help \
	--with-id3tag=system \
	--with-libmad=system \
	--with-libsndfile=system \
	--with-libflac=system \
	--with-vorbis=system

%{__make} \
	CCC="%{__cxx} -fno-exceptions -fno-rtti" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Multimedia,%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_PATH=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Multimedia
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

# not built in this version
#install audacity-help.htb $RPM_BUILD_ROOT%{_datadir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/audacity
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_applnkdir}/*/*
%{_pixmapsdir}/*
