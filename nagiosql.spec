# TODO:
#	- install dir - subpackage? how about doc? sql? ENABLE_INSTALLER?
#
%define		ver	302
Summary:	Web based administration tool for Nagios
Name:		nagiosql
Version:	3.0.2
Release:	0.1
License:	BSD
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/nagiosql/%{name}%{ver}.tar.bz2
# Source0-md5:	274a3b46db8151a89f5a3b47c69171f6
Source1:	%{name}-apache.conf
Source2:	%{name}.cfg
Patch0:		%{name}-paths.patch
URL:		http://www.nagiosql.org/
Requires:	php(ftp)
Requires:	php(gettext)
Requires:	php(mysql)
Requires:	php-pear-HTML_Template_IT
Requires:	webapps
Requires:	webserver(php) >= 4.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_webconfdir	%{_webapps}/%{_webapp}

%description
NagiosQL is a web based administration tool for Nagios 2 and Nagios 3.
It helps you to easily build a complex configuration with all options,
manage and use them. NagiosQL is based on a webserver with PHP, MySQL
and local file or remote access to the Nagios configuration files.

%prep
%setup -q -n %{name}3
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}/nagios,%{_sysconfdir}/%{name}/{,backup/}{hosts,services},%{_webconfdir}}

cp -a admin functions images install templates *.php *.ico $RPM_BUILD_ROOT%{_appdir}
cp -a config $RPM_BUILD_ROOT%{_webconfdir}
ln -sf %{_webconfdir}/config $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_webconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/nagios

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

if [ "$httpd_reload" ]; then
	%service httpd reload
fi
if [ "$apache_reload" ]; then
	%service apache reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc install/doc/*
%{_sysconfdir}/nagios/*
%attr(770,root,http) %{_sysconfdir}/%{name}
%dir %attr(750,root,http) %{_webconfdir}
# g+w required for install-time database configuration only
%dir %attr(1770,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webconfdir}/config
%dir %{_webconfdir}/config/locale
%lang(de) %{_webconfdir}/config/locale/de_DE
%lang(en) %{_webconfdir}/config/locale/en_GB
%lang(fr) %{_webconfdir}/config/locale/fr_FR
%lang(it) %{_webconfdir}/config/locale/it_IT
%lang(pl) %{_webconfdir}/config/locale/pl_PL
%lang(ru) %{_webconfdir}/config/locale/ru_RU
%lang(zh) %{_webconfdir}/config/locale/zh_CN
%{_webconfdir}/config/*.css
%{_webconfdir}/config/*.php
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webconfdir}/httpd.conf
%{_appdir}
