# WSO2 - Identity Server

A wso2 formula for install and configure WSO2 - Identity Server.

Note:

See the full [Salt Formulas installation and usage instructions](http://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html).


## Prerequisites 

###### Download
- [WSO2 - identity server, version 5.4.0](https://wso2.com/identity-and-access-management#download) .zip file from official product pages and save it to source files directory:

- [Java SE Development Kit 8u144](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-javase8-2177648.html?printOnly=1) .tar file from official product pages and save it to source files directory:

###### Salt-Master Configuration:
- set local direcotry for file server built into Salt master:
```
file_roots:
  base:
    - /srv/salt
```
- set remote file repository:
```
gitfs_remotes:
  - https://github.com/ssurmanek/wso2-formula.git
```

- enable both file servers:
```
fileserver_backend:
  - git
  - roots
```
