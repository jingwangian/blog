### Socket functions

1. socket function is defined as following:
``` C
int socket(int domain, int type, int protocol);
```

2. Bind socket to the specific network resource(address and port)
``` C
int bind(int socket, socketaddr *addr, int length);
```

3. Let the socket start to listen
``` C
int listen(int socket, int blacklog);
```

4. Accept a new connection request
``` C
int accept(int socket, sockaddr *from, int *fromlen);
```

	The function returns a new socket file descriptor which is used to communicate with the remote client. The original socket can still be used to listen for additional client connections.
    
5. Send a message to peer
``` C
int send(int socket, const void *message, int length, int flags);
```

6. Receive message from peer
``` C
int recv(int socket, void *message, int length, int flags);
```

7. Send a UDP message to peer
``` C
int sendto(int socket, const void *msg, int msglen, int flags, struct sockaddr *to, int tolen);
```

8. Receive UDP message from peer
``` C
int recvfrom(int socket, void *msg, int msglen, int flags, struct sockaddr *from, int fromlen);
```

9. get and set options on sockets
``` C
int getsockopt(int sockfd, int level, int optname, void *optval, socklen_t *optlen);
int setsockopt(int sockfd, int level, int optname, const void *optval, socklen_t optlen);
```

###reference:
1. https://www.ibm.com/support/knowledgecenter/en/ssw_i5_54/rzab6/xnonblock.htm
2. https://www.ibm.com/support/knowledgecenter/en/ssw_i5_54/rzab6/poll.htm
