# TODO:
# - install dir - subpackage? how about doc? sql? ENABLE_INSTALLER?
#
%define		ver	304
Summary:	Web based administration tool for Nagios
Name:		nagiosql
Version:	3.0.4
Release:	2
License:	BSD
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/nagiosql/%{name}%{ver}.tar.bz2
# Source0-md5:	32644a4ac38e94714d39af63456cb7a0
Source1:	%{name}-apache.conf
Source2:	%{name}.cfg
Source3:	%{name}-httpd.conf
Patch0:		%{name}-paths.patch
URL:		http://www.nagiosql.org/
Requires:	php(ftp)
Requires:	php(gettext)
Requires:	php(mysql)
Requires:	php(xml)
Requires:	php-pear-HTML_Template_IT
Requires:	webapps
Requires:	webserver(php) >= 4.3
Conflicts:	apache-base < 2.4.0-1
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
%setup -q -c
#-n %{name}
sed -i -e 's,\r$,,' install/sql/nagiosQL_v3_db_mysql.sql
%patch -P0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}/nagios,%{_sysconfdir}/%{name}/{,backup/}{hosts,services},%{_webconfdir}}

cp -a admin functions images install templates *.php *.ico $RPM_BUILD_ROOT%{_appdir}
cp -a config $RPM_BUILD_ROOT%{_webconfdir}
ln -sf %{_webconfdir}/config $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_webconfdir}/apache.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_webconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/nagios

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc install/doc/*
%{_sysconfdir}/nagios/*
%attr(2770,root,nagios-data) %{_sysconfdir}/%{name}
%dir %attr(750,root,http) %{_webconfdir}
# g+w required for install-time database configuration only
%dir %attr(1770,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webconfdir}/config
%dir %{_webconfdir}/config/locale
%lang(de) %{_webconfdir}/config/locale/de_DE
%lang(en) %{_webconfdir}/config/locale/en_GB
%lang(es) %{_webconfdir}/config/locale/es_ES
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
