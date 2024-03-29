# Docker Container Security - Part 1

As a result of my research on container security, i was able to figure out few different methods and configurations that can used to secure the containers. Here i am specifically talking about docker but the principles are same for every container tech. 

The first and most important part to understand the requirement. 
Containers are used to run all sort of things nowadays. There are positive and negative impacts of these from a security perspective. The positive thing is we can deploy application faster, share it easily and also can reduce the compatibility issue. The negative point is, it is easy to misconfigure containers which can result mild or serious security issues, for example one of the common misconfiguration with docker containers when exposing ports can bypass UFW firewall rules in Linux operating systems.

I'll divide my research findings into different parts to make it easy to understand. As this is the first part, here I'll go through some of the basic security configurations. Later on we can go through the container auditing methods and techniques, scanning, vulnerability analysis and of course some exploiting techniques. 

# RIGHT PRIVILEGES :- 

As i mentioned before, the first thing is to understand the requirements. 
It is not very common thing to see when we deploy a container, the default user is root. The question is do we need root access to run our applications? i would say it depends. Docker needs to have enough permissions to modify the host file system to run, otherwise, your container won't be initialized. I agree a lot of applications need root access to run but a good practice would to understand the application and set privileges. 


Setting "USER 1001" docker file can prevent the container from running as root. USER 1001: this is a non-root user UID, and here it is assigned to the image in order to run the current container as an unprivileged user.


# PRIVILEGED MODE :-

Running a container with privileged flag allows internal teams to have critical access to the host’s resources — but by abusing a privileged container, cybercriminals can gain access to them as well.
It is not always the case that, when an attacker abuses a privileged container for an attack, it does not necessarily have to be remote code execution. But when they do execute code, the potential attack surface is wide.

Setting the flag --security-opt=no-new-privileges at run time prevents the application processes inside the container from gaining new privileges during execution. 


# SETTING CAPABILITIES :-

Linux's capabilities are special attributes in the Linux kernel that grant processes and binary executables specific privileges that are normally reserved for processes whose effective user ID is 0 (The root user, and only the root user, has UID 0).

Limiting the capabilities to only necessary ones can add an extra layer of security. This can be implemented by dropping all the capabilities and then adding only the necessary ones. 
The capabilities in docker can be set during run time in docker by using the --cap flag

Dropping all capabilities

flag : --cap-drop all

Adding capabilities

flag: --cap-add 

Reference for Linux capabilities - https://man7.org/linux/man-pages/man7/capabilities.7.html


# RESTRICTING ACCESS TO FILE SYSTEMS :-

There are multiple ways to restrict access to file systems in docker container. Here we are gonna take a look at setting restricting permissions. We can run the docker container in read only mode, this will restrict the access to modify the file systems but the problem comes when the application is dynamic in nature. The solution here would be setting a temporary files systems to write data by the applications. Here the application can write to the temporary file system. Both restricting access and setting temporary file system can be done at run time.

Setting read only 

flag : --read-only 

Setting temporary file system

flag : --tmpfs 


example: docker run -td --read-only --tmpfs /opt 


# ISOLATING CONTAINER IF NECESSARY :-

There are many ways to isolate containers. Here we are going to take a look at restricting inter container communications. On upcoming parts we can take a look at other methods as well. One way to achieve this goal is through docker networking. 

The first step here is to do a docker network ls and then docker inspect bridge. We can see a lot of information but for now we are interested in below mentioned details. 

Options": {
	"com.docker.network.bridge.default_bridge": "true",
	"com.docker.network.bridge.enable_icc": "true",
	"com.docker.network.bridge.enable_ip_masquerade": "true",
	"com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
	"com.docker.network.bridge.name": "docker0",
	"com.docker.network.driver.mtu": "1500"
},

Here "com.docker.network.bridge.enable_icc": "true" is the option to enable or disable inter container communications. Setting "com.docker.network.bridge.enable_icc": "true" to false can restrict inter container communications. 

Now we should create a new network and restrict the inter container communication.


Create network with no inter container communication

docker network create --driver bridge "com.docker.network.bridge.enable_icc": "false" < network name >

Check 

docker inspect < network name >

Run the container with created network

Example

docker run -td --network < network name > <image>



The steps and methods mentioned here are some of the basic practices that can help to run containers in a secure way. The implementation of container security entirely depends on the nature of applications running in containers. We will take a deep look into more methods and techniques in upcoming parts.

