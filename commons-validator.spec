%bcond_with tests

Summary:        Commons Validator
Name:           commons-validator
Version:        1.4.0
Release:        5
License:        Apache License
Group:          Development/Java
Source0:        http://www.apache.org/dist/commons/validator/source/commons-validator-%{version}-src.tar.gz
Source1:        http://www.apache.org/dist/commons/validator/source/commons-validator-%{version}-src.tar.gz.asc
Source2:        %{name}.catalog
Patch0:		commons-validator-1.4.0-fix-javadoc.patch
URL:            https://commons.apache.org/proper/commons-validator/
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  jakarta-commons-beanutils >= 0:1.5
BuildRequires:  jakarta-commons-digester >= 0:1.3
BuildRequires:  jakarta-commons-logging >= 0:1.0.2
BuildRequires:  oro >= 0:2.0.6
BuildRequires:  junit >= 0:3.7
BuildRequires:  rhino
BuildRequires:  xml-commons-apis
BuildRequires:  xerces-j2
Requires:       jakarta-commons-beanutils >= 0:1.5
Requires:       jakarta-commons-digester >= 0:1.3
Requires:       jakarta-commons-logging >= 0:1.0.2
Requires:       oro >= 0:2.0.6
Requires:       rhino
BuildArch:      noarch
%rename jakarta-%name

%description
A common issue when receiving data either electronically or from user
input is verifying the integrity of the data. This work is repetitive
and becomes even more complicated when different sets of validation
rules need to be applied to the same set of data based on locale for
example. Error messages may also vary by locale. This package attempts
to address some of these issues and speed development and maintenance
of validation rules.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-src
%autopatch -p1

# Looks like upstream forgot to remove -SNAPSHOT from the version at
# release time...
sed -i -e 's,-SNAPSHOT,,g' build.xml

cp -p %SOURCE2 src/main/resources/org/apache/commons/validator/resources/catalog

# -----------------------------------------------------------------------------

%build
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
export CLASSPATH=%_datadir/java/ant.jar:%_datadir/java/ant-launcher.jar
ant -Dbuild.sysclasspath=ignore \
-Djunit.jar=%{_javadir}/junit.jar \
-Dcommons-beanutils.jar=%{_javadir}/commons-beanutils.jar \
-Dcommons-digester.jar=%{_javadir}/commons-digester.jar \
-Dcommons-logging.jar=%{_javadir}/commons-logging.jar \
-Doro.jar=%{_javadir}/oro.jar \
-Ddojo_custom_rhino.jar=%{_javadir}/rhino.jar \
-Dxerces.jar=%{_javadir}/xerces-j2.jar \
dist

%if %{with tests}
%check
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
export CLASSPATH=%_datadir/java/ant.jar:%_datadir/java/ant-launcher.jar
ant -Dbuild.sysclasspath=ignore \
-Djunit.jar=%{_javadir}/junit.jar \
-Dcommons-beanutils.jar=%{_javadir}/commons-beanutils.jar \
-Dcommons-digester.jar=%{_javadir}/commons-digester.jar \
-Dcommons-logging.jar=%{_javadir}/commons-logging.jar \
-Doro.jar=%{_javadir}/oro.jar \
-Ddojo_custom_rhino.jar=%{_javadir}/rhino.jar \
-Dxerces.jar=%{_javadir}/xerces-j2.jar \
test
%endif

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p dist/%{name}-%{version}-compress.js $RPM_BUILD_ROOT%{_javadir}/%{name}-compress-%{version}.js
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# data
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
(%{__mv} -f %{buildroot}%{_javadir}/*.js %{buildroot}%{_datadir}/%{name})

# dtds and catalog
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}
cp -p src/main/resources/org/apache/commons/validator/resources/{*.dtd,catalog} $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# fix end-of-line
%{__perl} -pi -e 's/\r\n/\n/g' *.txt

# -----------------------------------------------------------------------------

%post
# Note that we're using versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/catalog > /dev/null || :
fi

%postun
# Note that we're using versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --remove \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/catalog > /dev/null || :
fi

# -----------------------------------------------------------------------------

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%{_datadir}/%{name}
%{_datadir}/sgml/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

# -----------------------------------------------------------------------------




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.1-9mdv2011.0
+ Revision: 665810
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.1-8mdv2011.0
+ Revision: 606064
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.1-7mdv2010.1
+ Revision: 523007
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.3.1-6mdv2010.0
+ Revision: 425446
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0:1.3.1-5mdv2009.0
+ Revision: 221649
- rebuild
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3.1-4mdv2008.1
+ Revision: 120919
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3.1-3mdv2008.0
+ Revision: 87418
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.3.1-2mdv2008.0
+ Revision: 82605
- update to new version

* Wed May 16 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0:1.3.1-1mdv2008.0
+ Revision: 27417
- Updated to 1.3.1.
- Updated jakarta-commons-validator.catalog (new dtds).


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.3.0-1.2mdv2007.1
+ Revision: 143932
- rebuild for 2007.1
- Import jakarta-commons-validator

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:1.3-1.1mdv2006.0
- 1.3
- rebuild for libgcj.so.7

* Thu Aug 18 2005 David Walluck <walluck@mandriva.org> 0:1.1.4-1.1mdk
- 1.1.4

* Sun May 22 2005 David Walluck <walluck@mandriva.org> 0:1.1.3-1.1mdk
- release

* Wed Sep 08 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.1.3-1jpp
- Upgrade to 1.1.3

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.0.2-3jpp
- Rebuild with ant-1.6.2

