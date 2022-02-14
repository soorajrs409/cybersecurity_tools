# Docker security part - 3

Finally done with part-3 of docker security tips and tricks. Here we are going understand some methods that can used to set up various good security practices.   

Lets take a look at securing the Docker daemon today. The docker consists many important components, let's start with these components today.

## Important components of docker.

### Docker daemon

The docker daemon is a service that runs on our host operating system. It is an important component designed to run in the background, manages those containers using the Docker Remote API. It currently only runs on Linux because it depends on a number of Linux kernel features, but there are a few ways to run Docker on MacOS and Windows too.

### REST API

The Docker daemon itself exposes a REST API. From here, a number of different tools can talk to the daemon through this API.

### Docker CLI

The most widespread tool is the Docker CLI. It is a command line tool that lets us talk to the Docker daemon. When we install Docker, we get both the Docker daemon and the Docker CLI tools together.



## Docker over TLS

Docker’s API is completely unprotected by default except for filesystem permissions on its Unix socket. We should really think about setting up TLS when otherwise anyone with access to the TCP port could browse our Docker containers, start new ones, and run actions as root on our system. When the TLS is configured, clients will require to present a valid certificate that’s signed by the server’s certificate authority. To get this working, we need to create SSL certificates, then set up Docker Engine to require TLS connections. Docker CLI clients must also be adjusted to expect a TLS server. So let's take a look at how to set it up.

### Exposing the TCP socket

We can expose Docker's TCP socket by using the -H flag to define an extra endpoint when staring the dockerd process. This flag can be repeated multiple times. In this example, both the Unix socket and TCP socket will be available. Port 2375 is conventionally used for unencrypted Docker connections. Port 2376 should be used instead once TLS has been set up.

#### $ /usr/bin/dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375

We can configure Docker to use these flags automatically by modifying the Docker service definition. Adding an override in /etc/systemd/system/docker.service.d/override.conf that changes the ExecStart line:

#### [Service]
#### ExecStart=/usr/bin/dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375

Reload systemd to apply the changes.

#### $ sudo systemctl daemon-reload

### Creating our certificate authority 

Lets's begin by creating a Certificate Authority (CA) for our TLS configuration. We will use this CA to sign our certificates, the server will refuse to communicate with clients that present a certificate from a different CA. Here we are going to use openssl to generate the certificates. 

#### Generate the private key
#### $ openssl genrsa -aes256 -out ca-private.pem 4096

Enter the required info and the private key will be generated.

### Generating a Server Key and Certificate Signing Request

Next let's create a server key and a certificate signing request:.

#### Generate the server key
#### $ openssl genrsa -out server-key.pem 4096

#### Generate a certificate signing request
#### $ openssl req -subj "/CN=example.com" -sha256 -new -key server-key.pm -out request.csr

The certificate signing request (CSR) contains all the information needed to produce a signed certificate. It’s important to check the common name in the CSR is correct for our server. This is specified in the CN field as example.com above, we should set it to the Fully Qualified Domain Name (FQDN) for our server.

### Let's set up Certificate Extensions

We need to specify certificate extensions if we want to add another domain or use an IP address. Let's create an extensions file with subjectAltName and extendedKeyUsage fields to set this up.

#### $ echo subjectAltName = DNS:sub.example.com;IP=192.168.0.1 >> extfile.cnf
#### $ echo extendedKeyUsage = serverAuth >> extFile.cnf

This will additionally permit connections via sub.example.com and 192.168.0.1.

### Generating a Signed Certificate

Now let's combine all the components and generate a signed certificate.

#### $ openssl x509 -req -days 365 -sha256 \
####    -in request.csr \
####    -CA ca-public.pem \
####    -CAkey ca-private.pem \
####    -CAcreateserial \
####    -extfile extfile.cnf \
####    -out certificate.pem

This takes the certificate signing request, adds our extension file, and uses our CA’s keys to produce a signed OpenSSL certificate. We will need to supply the CA’s passphrase to complete the process. This certificate is set to expire after a year. We can adjust the -days flag to obtain a useful lifetime for our requirements. We should generate a replacement certificate before this one expires, which is usually done through scripts.

### Generating a Client Certificate

Next we should generate another certificate for our Docker clients to use. This must be signed by the same CA as the server certificate. Use an extensions file with extendedKeyUsage = clientAuth to prepare this certificate for use in a client scenario.

#### Generate a client key
#### $ openssl genrsa -out client-key.pem 4096

#### Create a certificate signing request
#### $ openssl req -subj '/CN=client' -new -key client-key.pem -out client-request.csr

#### Complete the signing
#### $ echo extendedKeyUsage = clientAuth >> extfile-client.cnf
#### $ openssl x509 -req -days 365 -sha256 \
####     -in client-request.csr \ 
####     -CA ca-public.pem \
####     -CAkey ca-private.pem \
####     -CAcreateserial \
####     -extfile extfile-client.cnf \
####     -out client-certificate.pem


### Let's configure Docker

Copy ca-public.pem, certificate.pem, and server-key.pem files into a new directory ready to reference in Docker config. Afterwards, copy the ca-public.pem, client-certificate.pem, and client-key.pem files to the machine which we will connect from. We can delete the certificate signing request and extension files in our working directory. Be careful not to lose the private keys as they’re non-recoverable. Without them we’ll be unable to validate certificates or generate renewals.

### Configuring the Docker Daemon

Now we can start the Docker daemon with TLS flags referencing our generated certificate and keys. The --tlscacert, --tlscert, and --tlskey parameters specify paths to the respective OpenSSL resources generated above.

#### $ /usr/bin/dockerd \
####    -H unix:///var/run/docker.sock \
####    -H tcp://0.0.0.0:2376 \
####    --tlsverify \
####    --tlscacert=ca-public.pem \
####    --tlscert=certificate.pem \
####    --tlskey=server-key.pem

Adding the --tlsverify flag enables enforcement of TLS connections. Clients without a matching certificate will be blocked from accessing Docker’s TCP socket.

### Configuring the Docker Client

Now let's activate TLS on the client by supplying TLS flags when we use the docker command. We must also add the -H flag to specify the remote Docker socket address to connect. From the client’s perspective, --tlsverify means the command will only connect to servers with a TLS certificate signed by the same certificate authority as its own.

#### $ docker \
####    -H tcp://0.0.0.0:2376 \
####    --tlsverify \
####    --tlscacert=ca-public.pem \
####    --tlscert=client-certificate.pem \
####    --tlskey=client-key.pem \
####    ps

Supplying these flags each time we use the CLI gets exhausting. If we’ll mostly be working with the same TLS-protected host, let's set the DOCKER_HOST and DOCKER_TLS_VERIFY environment variables in our shell profile. Copy the certificates files to ca, cert, and key inside our ~/.docker directory. These corresponds to Docker’s --tls flags and define a default certificate for the client.

#### $ export DOCKER_HOST=tcp://0.0.0.0:2376
#### $ export DOCKER_TLS_VERIFY=1

The Docker client also supports alternative verification modes, check here for more info - https://docs.docker.com/engine/security/protect-access/#other-modes. Using a mixture of tls, tlscacert, tlscert, tlskey, and tlsverify flags activates varying TLS enforcement levels.

With just tls set, Docker will authenticate the server using the default CA pool. Adding the tlscacert and tlsverify flags without a client key will enforce the server uses the given CA without any other checks. Omitting tlscacert and tlsverify but including the other three keys will verify the client’s certificate without authenticating the server’s CA.



## Using Namespaces 

Namespaces are a feature of the Linux kernel that partitions kernel resources such that one set of processes sees one set of resources and another set of processes sees a different set of resources.
One of the primary concerns when using containers is isolation between the containers and host as well as the isolation among different containers. Imagine that we spin up two containers with different sets of features and there is no need for each container process to know what’s running on the other container. This also prevents the attacker to gain root privileges incase on an container breakout. 

There are many namespaces, some of the important namespaces are listed below. We will take a look at each one them individually at a high level.

#### PID namespace for process isolation.
#### USER namespace for the user privilege isolation.
#### UTS namespace for isolating kernel and version identifiers.
#### IPC namespace for managing access to IPC resources.
#### MNT namespace for managing filesystem mount points.
#### NET namespace for managing network interfaces. 

### 1) PID namespace for process isolation

The PID namespace provides process isolation. When a container is created, the container process cannot see what processes are running on the host by default. Also any other container started on the host will not be able to see the list of processes running on other containers on the same host. But if we run a container with the same PID namesapce of any other container, here the container will the same list of running process. This can be done with the help of the below mentioned command,

#### $ docker run -it –pid=container:container1 –name container3 alpine sh

Here both container1 and container3 will be able to see each other's process. 

### 2) User namespace

Let's start with a scenario, we have built an application that is running inside a Docker container and the application is running with root privileges on the container. When starting this container, let us also assume that we have mounted the /bin directory of the host machine onto the container. In this scenario, if an attacker compromised this application and gained root access on the container, can this attacker modify files on the host’s /bin directory from within the container?

The answer is YES !!!!!  because USER namespaces are not enabled by default and thus the attacker will be able to modify the files owned by the root user on the host. This is because root users inside the container will have the same privileges as the root users on the host unless USER namespaces are enabled. 
So what's the solution for this? The solution is Enable USER namspaces.If we enable user namespaces for Docker daemon, it will ensure that the root inside the docker container is run in a separate context that is different from the host’s context.

Now lets's see how can configure it,

#### Stop the docker engine 
#### $ sudo systemctl stop docker  

Now let us start Docker daemon by using the following command.

#### $ sudo dockerd –userns-remap=default &  

This will start the Docker daemon in the background using the default user namespace mapping where the Docker map user and group are created and mapped to non-privileged UID and GID ranges in the /etc/subuid and /etc/subgid files.  
Since we have enabled user namespaces for the Docker daemon, when a root owned file from the host is mounted onto the container, the root user in the container will not have permission to modify this file owned by root on the host. This is because the mounted file exists in the local file system of the Docker host and the container doesn’t have root access outside of the namespace that it exists in. Though the container is running under the root user security context, this is only a root user within the scope of the namespace that the container is running in.

### 3) UTS namespace 

UTS stands for UNIX Time-sharing System Sharing and isolates system identifiers Domainname and Hostname. UTS namespace allows all containers to have a unique hostname. Bydefault, all containers will have a hostname with the first 12 characters of the container ID . It is also possible to assign a custom hostname to the container using the –hostname flag as follows.

#### $ docker run -it –hostname=customhost –name container4 alpine sh

### 4) IPC namespace

IPC(POSIX/SysV IPC)  namespace gives a process its own interprocess communication resources by providing separation of named shared memory segments, semaphores and message queues. 

### 5) MNT namespace

MNT namespace allows containers to have their own set of mounted file systems and root directories. Processes running in one MNT namespace cannot see the mounted file system of another MNT namespace. 

### 6) NET namespace

Let us consider the same scenario we discussed in the beginning of the article. Let us assume that there are 3 Apache web servers running in 3 different containers. All three containers will need to start the Apache servers on port 80. In addition to it, the host machine should also be able to use port 80 for another service. Network namespaces (NET namespace) allow processes inside each namespace instance to have access to a new IP address along with the full range of ports.


## Inter-container communication 

We can isolate docker containers from one another. This completely depends on our requirement, because sometimes it is required to enable to inter-container enabled. Docker does not isolate containers by default. In order to disable inter-container communication, we will need to create a new Docker network. This can be done by running the following command with the “icc” option set to false.

#### $ docker network create --driver bridge -o "com.docker.network.bridge.enable_icc"="false" <network-name>   

We can now run the container that we want to isolate with the following command:

#### $ docker run --network <network-name>


 That's the end of docker security part-3. On the next part let's take a look a some more interesting methods. 

