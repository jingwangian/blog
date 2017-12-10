#Using socket on TCP

### Build TCP Server
1. create a socket by using **socket** function
```C
#include <sys/types.h> 
#include <sys/socket.h> 
#include <stdio.h> 
#include <sys/un.h> 
#include <unistd.h> 
#include <stdlib.h>

server_sockfd = socket(AF_INET, SOCK_STREAM, 0);
```

2. bind the socket by using **bind** function
```C
struct sockaddr server_address;

server_address.sun_family = AF_INET;
strcpy(server_address.sun_path, “server_socket”);
server_len = sizeof(server_address);
bind(server_sockfd, (struct sockaddr *)&server_address, server_len);
```
3. start listen by using **listen** function
```C
listen(server_sockfd, 5);
```
4. Accept the request connection by using **accept**, and get a new socket
```C
struct sockaddr client_address;

client_len = sizeof(client_address); 
client_sockfd = accept(server_sockfd,
						(struct sockaddr *)&client_address, 
                        &client_len);
```
5. Using the **send/recv** on new socket to communicate with the client.
```C
len = send(fd, “Welcome to my server\n”, 21, 0)
while ((len = recv(fd, buf, BUFSIZ, 0)) > 0)
{
	...
}
```
6. Close socket by using **close** function
```C
close(fd);
```


### Build TCP Client 
1. create a socket
2. 



###reference:
1. https://www.ibm.com/support/knowledgecenter/en/ssw_i5_54/rzab6/xnonblock.htm
2. https://www.ibm.com/support/knowledgecenter/en/ssw_i5_54/rzab6/poll.htm
