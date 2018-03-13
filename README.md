# WSO2 - Identity Server

A wso2 formula for install and configure WSO2 - Identity Server.

Note:

See the full [Salt Formulas installation and usage instructions](http://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html).


## Prerequisites 

###### Download
- WSO2-IS .zip file from official product pages and save it to source files directory: [WSO2 - identity server, version 5.4.0](https://wso2.com/identity-and-access-management#download)

- JDK .tar file from official product pages and save it to source files directory: [Java SE Development Kit 8u144](http://www.oracle.com/technetwork/java/javase/downloads/java-archive-javase8-2177648.html?printOnly=1)

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

## Accessing
Management Console is accessible at url:

    https://localhost:9443/carbon

Administrator account default credentials:
- username: admin
- password: admin

# midPoint: the Identity Governance and Administration tool
## Info
MidPoint is open identity & organization management and governance platform which uses Identity Connector Framework (ConnId) and leverages Spring framework. It is a Java application deployed as a stand-alone server process. This image is based on official OpenJDK version 8 image which runs on Alpine Linux and deploys latest MidPoint version 3.7.1.

## Launch Container:
Download:
```
docker pull evolveum/midpoint
```
Run on port 8080:
```
docker run -p 8080:8080 evolveum/midpoint
```

## Access MidPoint:
URL: http://127.0.0.1:8080/midpoint
Admin username: Administrator
Admin password: 5ecr3t

## Access shell:
```
docker exec -it midpoint /bin/sh
```
