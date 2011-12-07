
# 
# The following is to make it easier to build/test alternate build 
# configurations.   The build_as_for... flags make it easy to try
# some predefined configurations.  No flag gets changed if it is already
# set, so that you can set flags at the command line and they won't 
# be changed by the following.
#
# 'bugzilla' = include some bugzilla configuration
#   'bugzilla_rhel' = include the RHEL bugzilla plugin and configuration
#         ELSE include the normal one.  This is ignored if 'bugzilla' not set
# 'strata' = include the strata plugin and RHEL configuration
#    'strata_test' = include the strata test configuration (ignored if !strata)
# 'obsolete_old_RHEL' = mark some particular older RHEL plugins as
#     obsolete, so they are removed during update
#     This flag and the obsoletes it protects can go away when this
#     is no longer an issue.
#

%if 0%{?rhel}
%define build_as_for_rhel 1
%endif

%if 0%{?build_as_for_rhel}
%if "%{?build_as_for_rhel_production}" == ""
%if "%{?build_as_for_rhel_test}" == ""
%define build_as_for_rhel_production 1
%endif
%endif
%endif

%if 0%{?build_as_for_rhel_production}
%if "%{?bugzilla}" == ""
%define bugzilla 0
%endif
%if "%{?bugzilla_rhel}" == ""
%define bugzilla_rhel 0
%endif
%if "%{?strata}" == ""
%define strata 1
%endif
%if "%{?strata_test}" == ""
%define strata_test 0
%endif
%if "%{?obsolete_old_RHEL}" == ""
%define obsolete_old_RHEL 1
%endif

%else
%if 0%{?build_as_for_rhel_test}
%if "%{?bugzilla}" == ""
%define bugzilla 1
%endif
%if "%{?bugzilla_rhel}" == ""
%define bugzilla_rhel 1
%endif
%if "%{?strata}" == ""
%define strata 0
%endif
%if "%{?strata_test}" == ""
%define strata_test 0
%endif
%if "%{?obsolete_old_RHEL}" == ""
%define obsolete_old_RHEL 1
%endif

%else
# then for everything else
%if "%{?bugzilla}" == ""
%define bugzilla 1
%endif
%if "%{?obsolete_old_RHEL}" == ""
%define obsolete_old_RHEL 0
%endif

%endif
%endif

Name:           report
Version:        0.18
Release:        7%{?dist}
Summary:        Incident reporting library

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://fedorahosted.org/report
Source0:        http://fedorahosted.org/released/report/%{name}-%{version}.tar.gz
Patch0: ftp_plugin_crash.patch
Patch1: production_strata.patch
Patch2: handle_self_signed_certs.patch
Patch3: setup_URL_translation.patch
Patch4: xml_html_formating.patch
Patch5: ftp_deps.patch
Patch6: plugin_config_exceptions.patch
Patch7: report_cmd_check_arg_access.patch
Patch8: strata_plugin_attach_separate_file.patch
Patch9: gtkio_clickable_button.patch
Patch10: scp_password_only_auth.patch
Patch11: GTKIO-success-dialog.patch
Patch12: remove-http-headers-from-user-display.patch
Patch14: correct-target-order.patch
Patch15: correct-how-we-are-gathering-Product-and-Version-inf.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: python-report = %{version}-%{release} 
Provides: report-devel = %{version}-%{release} 

BuildRequires: python-devel
BuildRequires: openssl-devel
BuildRequires: libxml2-devel
BuildRequires: gettext
%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRequires: curl-devel
%else
BuildRequires: libcurl-devel
%endif  

Requires: openssl report-config-scp report-config-localsave report-config-ftp
Requires: libcurl
Requires: libxml2

%if ! 0%{?bugzilla}
Provides: report-config-default
%else
Requires: report-config-default
%endif

%if 0%{?obsolete_old_RHEL}
%if ! 0%{?bugzilla}
Obsoletes: report-plugin-RHEL < %{version}-%{release}
Obsoletes: report-config-RHEL < %{version}-%{release}
Obsoletes: report-plugin-RHEL-bugzilla < %{version}-%{release}
Obsoletes: report-config-RHEL-bugzilla-redhat-com < %{version}-%{release}
%else
%if ! 0%{?bugzilla_rhel}
Obsoletes: report-plugin-RHEL-bugzilla < %{version}-%{release}
Obsoletes: report-config-RHEL-bugzilla-redhat-com < %{version}-%{release}
%endif
%endif
%endif




%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif



%description
A generic problem/bug/incident/error reporting library, that can be 
configured to deliver a report to a variety of different ticketing 
systems.

%package gtk
Summary:        GTK IO for reporting library
Group:          System Environment/Libraries

Requires: pygtk2
Requires: report = %{version}-%{release}

%description gtk
Provides GTK IO dialogs for the reporting library

%package newt
Summary:        Newt IO for reporting library
Group:          System Environment/Libraries

Requires: newt-python
Requires: report = %{version}-%{release}

%description newt
Provides Newt IO dialogs for the reporting library

%if 0%{?bugzilla}
%if 0%{?bugzilla_rhel}
%package plugin-RHEL-bugzilla
Summary:        Plugin template reporter to RHEL
Group:          System Environment/Libraries

Requires: report = %{version}-%{release}
Requires: rpm-python
%if 0%{?obsolete_old_RHEL}
Obsoletes: report-plugin-RHEL
%endif

%description plugin-RHEL-bugzilla
Plugin template reporter to bugzilla within RHEL

%else
%package plugin-bugzilla
Summary:        Plugin template reporter to bugzilla
Group:          System Environment/Libraries

Requires: report = %{version}-%{release}
Requires: rpm-python
Requires: python-bugzilla

%description plugin-bugzilla
Plugin template reporter to bugzilla
%endif
%endif

%package plugin-ftp
Summary:        Plugin template reporter to ftp
Group:          System Environment/Libraries

Requires: report = %{version}-%{release}

%description plugin-ftp
Plugin template reporter to ftp

%package plugin-scp
Summary:        Plugin template reporter to scp
Group:          System Environment/Libraries
Requires: report = %{version}-%{release}

%description plugin-scp
Plugin template reporter to scp

%package plugin-localsave
Summary:        Plugin template reporter to local directory
Group:          System Environment/Libraries
Requires: report = %{version}-%{release}

%description plugin-localsave
Plugin template reporter to localsave

%package config-ftp
Summary:        Config for reporter to ftp
Group:          System Environment/Libraries
Requires: report-plugin-ftp = %{version}-%{release}

%description config-ftp
Config for reporter to ftp

%package config-scp
Summary:        Config for reporter to ftp
Group:          System Environment/Libraries
Requires: report-plugin-scp = %{version}-%{release}

%description config-scp
Config for reporter to scp

%package config-localsave
Summary:        Config for reporter to ftp
Group:          System Environment/Libraries
Requires: report-plugin-localsave = %{version}-%{release}

%description config-localsave
Config for reporter to local directory

%if 0%{?bugzilla}
%if 0%{?bugzilla_rhel}
%package config-RHEL-bugzilla-redhat-com
Summary:        Config for reporter to bugzilla.redhat.com within RHEL
Group:          System Environment/Libraries
Requires: report-plugin-RHEL-bugzilla = %{version}-%{release}
Provides: report-config-default = %{version}-%{release}
%if 0%{?obsolete_old_RHEL}
Obsoletes: report-config-RHEL
%endif

%description config-RHEL-bugzilla-redhat-com
Config for reporter to bugzilla.redhat.com within RHEL

%else
%package config-bugzilla-redhat-com
Summary:        Config for reporter to bugzilla.redhat.com
Group:          System Environment/Libraries
Requires: report-plugin-bugzilla = %{version}-%{release}
Provides: report-config-default = %{version}-%{release}

%description config-bugzilla-redhat-com
Config for reporter to bugzilla.redhat.com
%endif
%endif

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch14 -p1
%patch15 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

%if 0%{?bugzilla} 
%if ! 0%{?bugzilla_rhel}
rm $RPM_BUILD_ROOT%{_sysconfdir}/report.d/RHEL-bugzilla.redhat.com.conf
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/report/plugins/RHEL-bugzilla
%else
rm $RPM_BUILD_ROOT%{_sysconfdir}/report.d/bugzilla.redhat.com.conf
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/report/plugins/bugzilla
%endif
%else
rm $RPM_BUILD_ROOT%{_sysconfdir}/report.d/RHEL-bugzilla.redhat.com.conf
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/report/plugins/RHEL-bugzilla
rm $RPM_BUILD_ROOT%{_sysconfdir}/report.d/bugzilla.redhat.com.conf
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/report/plugins/bugzilla
%endif

%if ! 0%{?strata}
rm -rf $RPM_BUILD_ROOT%{_bindir}/strata
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/report/plugins/strata
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/report.d/RHEL.conf
%endif
%if ! 0%{?strata_test}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/report.d/strata-test.conf
%endif


mkdir -p $RPM_BUILD_ROOT/var/%{name}



%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README LICENCE
%dir %{python_sitearch}/report
%{python_sitearch}/report/__init__.py*
%{python_sitearch}/report/accountmanager.py*
%{python_sitearch}/report/release_information.py*
%dir %{python_sitearch}/report/io
%{python_sitearch}/report/io/__init__.py*
%{python_sitearch}/report/io/TextIO.py*
%dir %{python_sitearch}/report/plugins
%{python_sitearch}/report/plugins/__init__.py*
%dir %{_sysconfdir}/report.d
%{_bindir}/report
%{_mandir}/man1/report.1.gz
%{_mandir}/man5/report.conf.5.gz
%dir %{_var}/report
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/report.conf

%{_includedir}/strata_client.h
%{_libdir}/libstrata_client.a
%{_libdir}/libstrata_client.la
%{_libdir}/libstrata_client.so
%{_libdir}/libstrata_client.so.0
%{_libdir}/libstrata_client.so.0.0.0
%if 0%{?strata}
%{python_sitearch}/report/plugins/strata
%config(noreplace) %{_sysconfdir}/report.d/RHEL.conf
%if 0%{?strata_test}
%config(noreplace) %{_sysconfdir}/report.d/strata-test.conf
%endif
%endif

%files gtk
%defattr(-,root,root,-)
%{python_sitearch}/report/io/GTKIO.py*

%files newt
%defattr(-,root,root,-)
%{python_sitearch}/report/io/NewtIO.py*

%files plugin-ftp
%defattr(-,root,root,-)
%{python_sitearch}/report/plugins/ftp

%files plugin-scp
%defattr(-,root,root,-)
%{python_sitearch}/report/plugins/scp

%files plugin-localsave
%defattr(-,root,root,-)
%{python_sitearch}/report/plugins/localsave

%if 0%{?bugzilla}
%if 0%{?bugzilla_rhel}
%files plugin-RHEL-bugzilla
%defattr(-,root,root,-)
%{python_sitearch}/report/plugins/RHEL-bugzilla

%else
%files plugin-bugzilla
%defattr(-,root,root,-)
%{python_sitearch}/report/plugins/bugzilla
%endif
%endif

%files config-ftp
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/report.d/ftp.conf

%files config-scp
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/report.d/scp.conf

%files config-localsave
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/report.d/localsave.conf

%if 0%{?bugzilla}
%if 0%{?bugzilla_rhel}
%files config-RHEL-bugzilla-redhat-com
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/report.d/RHEL-bugzilla.redhat.com.conf

%else
%files config-bugzilla-redhat-com
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/report.d/bugzilla.redhat.com.conf
%endif
%endif


%changelog
* Mon Aug 20 2010 Gavin Romig-Koch <gavin@redhat.com> 0.18-7
- correct how we are gathering Product and Version information (RHEL 625109)

* Mon Aug 10 2010 Gavin Romig-Koch <gavin@redhat.com> 0.18-6
- Correct the order of target choices
- remove http headers from user display (RHEL 621354)
- correct GTKIO success dialog box (partial RHEL 621354)

* Tue Jul 20 2010 Gavin Romig-Koch <gavin@redhat.com> 0.18-5
- scp plugin: force password auth (RHEL 589702)
- fix known hosts bug for strata scp target (RHEL 589702)
- GTKIO: only show 'clickable' button if displaying the link is possible (RHEL 594827)
- strata client needs to attach each file as separate file (RHEL 591922)
- report cmd: check access to file immediatly (RHEL 614274)
- Report throws traceback when there is a configuration for a non-present plugin (RHEL 614139)

* Wed Jul 14 2010 Gavin Romig-Koch <gavin@redhat.com> 0.18-4
- Include the ftp target and plugin in all installs (RHEL 614094)

* Mon Jul 12 2010 Gavin Romig-Koch <gavin@redhat.com> 0.18-3
- correct Obsoletes for report-*-RHEL-*
- strata: handle self signed certs
- strata-test.conf: setup URL translation
- add html and xml response translation to strata_client_lib

* Fri Jul 09 2010 Gavin Romig-Koch <gavin@redhat.com> 0.18-2
- fix crash in ftp plugin (Fedora 610870)(RHEL 609480)
- Production/GA configuration of report, enable Strata plugin (RHEL 567972)
 
* Thu Jun 29 2010 Gavin Romig-Koch <gavin@redhat.com> 0.18-1
- strata plugin buttonURLXxxx (RHEL 589704)
- improve strata server testing scripts
- reorg functions in strata_client_lib (RHEL 591922 related)
- improved error checking of C compiler
- Eliminate crash in DisplayXXXMessage

* Thu Jun 24 2010 Gavin Romig-Koch <gavin@redhat.com> 0.17-1
- better fix for bug in localsave to /tmp
    (Fedora 595854)(RHEL 595855)(RHEL 607507)
- Revert "fix bug in localsave to /tmp (Fedora 595854)(RHEL 595855)"
- correct SyntaxWarning: name 'HAVE_gnomekeyring' is used prior to
    global declaration. (Fedora 604235)
    Author: Ales Kozumplik <akozumpl@redhat.com>
- l10n: Updates to Polish (pl) translation
    Author: raven <raven@fedoraproject.org>
- l10n: Updates to Ukrainian (uk) translation
    Author: yurchor <yurchor@fedoraproject.org>

* Sat Jun 19 2010 Gavin Romig-Koch <gavin@redhat.com> 0.16-1
- Insure correct PRODUCT and VERSION used in the Bugzilla and Strata plugins 
      under Anaconda (RHEL 586147)
- Prepare for the switch from RHEL-bugzilla to Strata (RHEL 567972 partial)
- allow canceling out of input with ctrl-D (RHEL 604030)
- pretty up Newt IO a bit (RHEL 603067)
- clean up documentation a bit (RHEL 604045)
- remove the unused 'username' command line and configuration option. 
      (RHEL 604195)
- fix the worst of the problems with the ftp plugin (RHEL 604782)(RHEL 604780)
- Need to add -DFORTIFY_SOURCE=2 (RHEL 599342)
- fix command line crash on empty or non-existant input file 
    (RHEL 594892)(Fedora 594890)
    with help from Adam Stokes <astokes@redhat.com>
- make target buttons list vertically, improve 'Query' titles 
    (RHEL 594897)(Fedora 594895)
- change the config file parser to make config names case sensitive 
    (Fedora 594863)(RHEL 594865)
    from Adam Stokes <astokes@redhat.com>
- change "localsave" button to "local" (Fedora 594899)(RHEL 594901)
    from Adam Stokes <astokes@redhat.com>
- fix bug in localsave to /tmp (Fedora 595854)(RHEL 595855)
    from Adam Stokes <astokes@redhat.com>
- Strata client now handles 305 redirects (RHEL 591907)
- Add po/ru.po to the list of PO files
- fix so that we continue to build on RHEL/EPEL-5: old libcurl version
- l10n: Updates to Ukrainian (uk) translation
    from yurchor <yurchor@fedoraproject.org> -

* Thu May 20 2010 Gavin Romig-Koch <gavin@redhat.com> 0.15-1
- Update version after release
- fixed: subpackage name change causes dependency failures (RHEL 594047)

* Wed May 19 2010 Gavin Romig-Koch <gavin@redhat.com> 0.14-1
- Improvements to the strata client testing scripts
- Corrections to prevent crashes when no user i/o is available (RHEL 589714)
- Alter the bugzilla plugin to handle reports that have missing fields 
     (like hashmarkername) (Fedora 585792)(RHEL 592641)
- Gnomekeyring now works for any application that uses GTKIO. 
     (RHEL 589697)(Fedora 589695)
- Allow the URL for the Strata plugin to be configurable
- Updates to the strata client to follow changes to the strata server
- Rename targets, and plugins for RHEL (to RHEL-bugzilla),
     and Strata (to RHEL-strata) (RHEL 591281)
- Gracefully handle missing or unreadable config files
     (RHEL 592602) (Fedora 592601) (RHEL 592485)
- Added Russian (from ypoyarko <ypoyarko@fedoraproject.org>) 
- Don't present 'save to keyring' checkbox if gnomekeyring is not installed
     (RHEL 591323)
- Correct handling of error messages from the strata server 
     (RHEL 591920)
- Updates to Polish (pl) translation (from raven <raven@fedoraproject.org>)
- Updates to Ukrainian (uk) translation (from <yurchor@fedoraproject.org>)
- Add basic http auth to report/strata-client (RHEL 592006)

* Wed May 12 2010 Gavin Romig-Koch <gavin@redhat.com> 0.12-1
- correct summary and description for strata client (RHEL 589707)
- remove component from bz query (Fedora 561830)
- add product, version, and component to strata create case (RHEL 590180)
- correct bug in report file parsing
- added pl lang
- update PO files
- fix memory leak: free attach_reponse in send_report_to_new_case
- a number of minor cleanups 
  - make it easy to build the RHEL configuration on Fedora for testing
  - add --gtk option to bin/report to improve ability to test
  - clean up _add_binding_from_string/isbinary problem
  - remove unused/unneeded patches from source repo
  - add example script showing htmlErrors
  - correct strata_client.h double underscores to single underscores
  - rename response_data to createcase_response in send_report_to_new_case
  - clean up warnings in strata_client code
  - correct/update strata testing scripts

* Thu May 06 2010 Gavin Romig-Koch <gavin@redhat.com> 0.11-1
- many minor changes to keep up with strata server
    including set the 'Accepted-Language:' header in the strata client 
       (Fedora BZ 575819)
- initial Polish translation
    from raven <raven@fedoraproject.org> 
- fix python config in spec file and makefiles so that both x86 
    and x86_64 arches can be installed at the same time.  (RHEL BZ 586971)
- corrects the password remembering/forgetting code for bugzilla.redhat.com
    and sealert (RHEL BZ 576632)
- Spanish translation
    from logan <logan@fedoraproject.org>
- Ukrainian (uk) translation
    from yurchor <yurchor@fedoraproject.org> 
- deal gracefully with non-openable/readable files in 
    NamedFileSignatureValues (Fedora BZ 573037)
- minor makefile and spec file changes:
    upgrade version
    change RHEL-6-build to RHEL-6-candidate
    add more mock makefile rules for more configurations

* Mon Apr 5 2010 Adam Stokes <ajs@redhat.com> 0.10-5
- Resolves: bz579045

* Tue Mar 30 2010 Adam Stokes <ajs@redhat.com> 0.10-2
- Update bz filer to submit correct product/version
- Complete move from templates to plugins

* Thu Mar 25 2010 Gavin Romig-Koch <gavin@redhat.com> 0.10-1
- Resolves: rhbz#576927
- Resolves: rhbz#576926
- Resolves: rhbz#576997
- Resolves: rhbz#576995
- simplify/correct interdependancies among report's sub-packages
- don't install the strata report plugin (but leave the client library)

* Wed Mar 24 2010 Adam Stokes <ajs@redhat.com> 0.9-2
- Update translation scheme
- Renamed ini to conf
- Renamed templates dir to plugins
- Defined target/plugins

* Tue Mar 23 2010 Gavin Romig-Koch <gavin@redhat.com> 0.9-1
- Resolves: rhbz#562655
- Update to new version in prep for release

* Fri Mar 19 2010 Adam Stokes <ajs@redhat.com> 0.8-5
- report.conf manpage
- report manpage
- do not traceback on empty login
- ask for existing strata case
- setting of config options overrides previous parameter
  if defined.

* Tue Mar 16 2010 Gavin Romig-Koch <gavin@redhat.com> 0.8-4
- add Strata client
- add serialize to report/signature file and read from report/signature file

* Wed Mar 11 2010 Adam Stokes <ajs@redhat.com> 0.8-3
- wrapper function to print to syslog and display io
- build plugins/configs based on distro
- makefile targets for el5.x86/x86_64 el6.x86/x86_64
- copyright addition to bin
- updated createfilesignature to accept binary bool

* Tue Mar 02 2010 Adam Stokes <ajs@redhat.com> 0.8-2
- move all alternatives into templates
- templates accepts overrides from cmdline
- new template ftp

* Thu Feb 11 2010 Gavin Romig-Koch <gavin@redhat.com> 0.8-1
- upgrade to 0.8
- add examples/IOtest.py
- add report/io/NewtIO
- have all GTK dialogs open in the center of the screen
- consistantly return True/False/None from io.functions and report
- add Provides: report-config-default
- minor improvements to makefile
- replace autogen.sh with a better makefiles system
- improved error message when scp plugin fails

* Thu Jan 28 2010 Gavin Romig-Koch <gavin@redhat.com> 0.7-1
- upgrade to 0.7
- correct the Requires: for config-RHEL
- improve localcopy plugin

* Mon Jan  4 2010 Gavin Romig-Koch <gavin@redhat.com> 0.6-1
- Add suffix to files in '/etc/report.d/'
- Create RHEL-template which doesn't depend on a separate python-bugzilla
- Correct bugs in report::report template loading which caused the same
   template to be loaded multiple times, and the wrong templates to be used
- Correct a open file leak
- Merge the fastback command into report
- Rename fastback to report-sendfile
- Correct button response bugs in GTKIO

* Thu Dec 17 2009 Gavin Romig-Koch <gavin@redhat.com> 0.5-1
- More cleanups/corrections from Fedora review:
  - added provides for python-report
  - reorg'd sub-package specfile sections to be more std
  - correct sub-package use of Build* and Requires:
  - include LICENCE text in both dist tarball and rpms.
  - other minor cleanups

* Thu Dec 10 2009 Gavin Romig-Koch <gavin@redhat.com> 0.5-1
- convert alternatives/redhat_bugzilla to templates/bugzilla-template

* Tue Dec 08 2009 Gavin Romig-Koch <gavin@redhat.com> 0.4-2
- Cleanups/Corrections from Fedora review:
  - Added GPL2 Licencing file and headers
  - removed unnecessary catcut plugin
  - correct Source0: and Group: headers
  - other misc. spec file problems

* Tue Dec 01 2009 Gavin Romig-Koch <gavin@redhat.com> 0.4-1
- Split out the GTK IO into its own rpm
- Split out the bugzilla and catcut plugins into their own rpms

* Mon Nov 23 2009 Gavin Romig-Koch <gavin@redhat.com> 0.3-1
- Convert to using Autotools

* Wed Nov 18 2009 Gavin Romig-Koch <gavin@redhat.com> 0.2-1
- significant changes

* Wed Oct 28 2009 Gavin Romig-Koch <gavin@redhat.com> 0.1-1
- initial version

