jdk:
  archive.extracted:
    - name: /opt/jdk/
    - source: salt://wso2is/files/jdk-8u144-linux-x64.tar.gz
    - archive_format: tar
    - if_missing: /opt/jdk/jdk1.8.0_144
    
java-alternatives:
  alternatives.install:
    - name: java
    - link: /usr/bin/java
    - path: /opt/jdk/jdk1.8.0_144/bin/java
    - priority: 100
    - require: 
      - archive: jdk
    
javac-alternatives:
  alternatives.install:
    - name: javac
    - link: /usr/bin/javac
    - path: /opt/jdk/jdk1.8.0_144/bin/javac
    - priority: 100
    - require: 
      - archive: jdk

java_home_env_variable:
  environ.setenv:
     - name: JAVA_HOME
     - value: /opt/jdk/jdk1.8.0_144
     - update_minion: True

wso2is:
  archive.extracted:
    - name: /opt/
    - source: salt://wso2is/files/wso2is-5.4.0.zip
    - archive_format: zip
    - if_missing: /opt/wso2is-5.4.0/
    
wso2is-start:
  cmd.run:
    - name: "./wso2server.sh --start"
    - cwd: "/opt/wso2is-5.4.0/bin/"
    - shell: /bin/bash
    - require: 
      - archive: jdk
      - archive: wso2is
