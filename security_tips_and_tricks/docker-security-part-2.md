# Docker security - Part 2

On part 1 of the Docker security, we took a look into various basic methods to ensure the security of the containers. Here we will go through some techniques and methods to verify the security as well as few auditing techniques.

Before diving deeper into the securing the containers, let's take a look into the question of what needs to be secured ?. The answer to this question can be very flexible depending upon the nature of the containers we are running or the pieces of software running inside the containers. There are few security measures that applies to all kind of containers. So let's take a look into it. 


# What needs to be secured??

1) The Docker host

2) The Docker daemon

3) containers

4) Communication between the components of the docker platform

5) Registry


Let's take a look at securing docker host. Since docker needs a host to run, it's important to make sure the host is secured enough. So here we are going to go through the host security and in the subsequent parts of the article we can cover the rest of the security measures.

# Host security

Host security is a huge topic and contains many practices to ensure security. Many of those are operating system dependent, we can take a look into some important and common practices.  

## 1) Host operating system

We have to understand the fact that docker containers are only as secured as the host operating system. So it's obvious that if the host is compromised, the docker is also compromised.
One of the best practices is to use a minimal operating system exclusively for docker. We know that no matter how much we spend time and effort in security, there's always a zero-day. Using a minimal OS can help in reducing the vulnerabilities caused by other softwares or services which are not really important to run. 
There are OS which are specifically designed for docker such as  Project Atomic, RancherOS, Alpine Linux, core OS etc., a lot of organizations use these to run docker in production. Again, the point to note here is, it doesn't matter what OS is used for running docker, what matters is how securely the OS is configured.
The below-mentioned article has very good tips for securing Linux host

reference link - https://linoxide.com/ultimate-guide-secure-ubuntu/


## 2) Auditing 

The auditing plays an important role in the cybersecurity. It is very good practice to log all the necessary information and audit the logs in certain interval of time. Nowadays, a lot of organizations are using the concept of offsite logging where they send the logs to an external server, the good thing about offsite logging is in case if the server is compromised and the attacker manage to delete the log, we still have a copy of the logs for the cyber forensic team to analyze.

## Auditing Tools

### Lynis 

lynis is a security auditing tool for Unix based systems. lynis follows a modular and opportunistic scanning technique, this means it will only use and test the components that it can find, such as the available system tools and its libraries. Another benefit of using lynis is it doesn't require any other tools for the purpose of auditing. lynis scan will give an overview of the benchmarks, not all the results are actionable, but it's worth to check and make sure security configurations are in place. 

### Lynis installation

sudo apt install lynix

### Lynis Usage 

sudo lynis audit system



### Tiger (security auditing and intrusion detection tools for Linux)

Tiger is a free, open-source collections of shell scripts for security audit and host intrusion detection, for Unix-like systems such as Linux. Tiger also uses chkrootkit and tripwire to scan and gather information about the host. 

### Tiger installation

sudo apt install tiger

### Usage

sudo tiger

When the security scan is complete, a security report will be generated in the log subdirectory. The scanning with tiger can be expanded and customized. Please refer to the below-mentioned article for more info about tiger.

tiger reference link - https://www.tecmint.com/tiger-linux-security-audit-intrusion-detection-tool/



### docker-bench-security

docker-bench-security is one of the most common tool used for auditing docker security and is a shell script for scanning the host and making the report of misconfigurations and vulnerabilities in both docker setup and host. docker-bench-security is available on github. 

github - https://github.com/docker/docker-bench-security

### docker-bench-security installation

sudo git clone https://github.com/docker/docker-bench-security

### Usage

sudo ./docker-bench-security.sh (for docker security auditing)

sudo ./docker-bench-security.sh -c host_configuration (for auditing host security)


## 3) Setting auditing rules

Auditing rules is one of the important method which helps in maintaining the security practices efficiently. It helps to get more accurate results very fast. Here we are going to use auditd for creating audit rules and for monitoring binaries and user interactions on a host

### Auditd

Auditd is short for Linux Audit Daemon. Auditd provides the user a security auditing aspect in Linux. The logs that are collected and saved by auditd, are different activities performed in the Linux environment by the user and if there is a case where any user wants to inquire what other users have been doing in a corporate or multiple-user environment, that user can gain access to this kind of information in a simplified and minimized form, which are known as logs. Also, if there has been an unusual activity on a user’s system, let’s say his system was compromised, then the user can track back and see how its system was compromised and this can also help in many cases for incident responding.

### Auditd installation

sudo apt install auditd

### Auditd setup

sudo systemctl start auditd

sudo systemctl enble auditd

### check status

sudo systemctl status auditd

### checking reports

sudo aureport

### example aureport 

Summary Report
======================
Range of time in logs: 20/10/21 12:48:16.134 - 20/10/21 12:48:36.864
Selected time for report: 20/10/21 12:48:16 - 20/10/21 12:48:36.864
Number of changes in configuration: 3
Number of changes to accounts, groups, or roles: 0
Number of logins: 0
Number of failed logins: 0
Number of authentications: 0
Number of failed authentications: 0
Number of users: 2
Number of terminals: 4
Number of host names: 1
Number of executables: 3
Number of commands: 2
Number of files: 0
Number of AVC's: 0
Number of MAC events: 0
Number of failed syscalls: 0
Number of anomaly events: 0
Number of responses to anomaly events: 0
Number of crypto events: 0
Number of integrity events: 0
Number of virt events: 0
Number of keys: 0
Number of process IDs: 6
Number of events: 17


### create audit rules 

This will watch and logs the binary execution. 

sudo auditctl -w <bin to be watched> -k <alias or name >

example: sudo auditctl -w /usr/bin/docker -k myDocker

### listing the logs 

sudo aureport -k

### making audit rules persistent 

By default, the audit rules are not persistent, so if the auditd restarts all the rules we added are gone. we can easily make it persistent by adding the rules in /etc/audit/rules.d/audit.rules

i) list the rules 

sudo auditctl -l

ii) copy the output and paste it at the last line of /etc/audit/rules.d/audit.rules and that's it. Now the rules are persistent. 



Here we have covered some of the important factors of securing the host for running containers and some auditing practices that can help in running containers securely. On the next part we can go through securing the docker daemon. 

reference for security configuration ubuntu - https://linoxide.com/ultimate-guide-secure-ubuntu/
