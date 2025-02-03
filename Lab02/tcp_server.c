/* A simple server in the internet domain using TCP
 * Answer the questions below in your writeup
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
    /* 1. What is argc and *argv[]?
     * argc is an integer whose value represents the number of command-line arguments that are passed to the program, 
     this is known as the argument count. *argv[] is an array of strings that represents the command-line arguments. The first value in the array 
     (argv[0]) is the program name, while the following values stored in the array represent additional arguments.
     */ 
    int sockfd, newsockfd, portno;
    /* 2. What is a UNIX file descriptor and file descriptor table?
     * A UNIX file descriptor is a unique integer identifier handle 
     that is used by the operating system in order to reference opened files, 
     other I/O resources, or sockets. A file descriptor table is a data structure 
     that is maintained via the operating system that essentially maps file descriptors to open file descriptions.  
     */
    socklen_t clilen;

    struct sockaddr_in serv_addr, cli_addr;
    /* 3. What is a struct? What's the structure of sockaddr_in?
     * A struct is a data structure that is user-defined in C in which groups variables under one name. This in hand helps with organization.
        serv_addr, cli_addr; make up the structure of sockaddr_in. Which includes the server’s address and the client’s address
     */
    
    int n;
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    /* 4. What are the input parameters and return value of socket()
     * The input parameters of the socket() are AF_INET, which specifies the IPv4 protocol family; 
     SOCK_STREAM, which specifies the stream socket type (TCP connection); and 0 while selects the default 
     protocol for the specified combination of domain and type stated earlier. The return value of socket is an 
     integer that represents a file descriptor for the created socket. If the method fails, it will return “-1.”
     */
    
    if (sockfd < 0) 
       error("ERROR opening socket");
    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
             sizeof(serv_addr)) < 0) 
             error("ERROR on binding");
    /* 5. What are the input parameters of bind() and listen()?
     * bind() has the input parameters sockfd, which represents the file 
     descriptor of the socket; (struct sockaddr *)&serv_addr, which is a 
     pointer to the sockaddr struct which contains the address and port to bind the socket; 
     and sizeof(serv_addr), which represents the size of the sockaddr_in strtuct.
     listen() has the input parameter sockfd, which is the file descriptor of the socket,
      and 5, which represents the backlog (the maximum number of pending connections that are allowed in the queue)
     */
    
    listen(sockfd,5);
    clilen = sizeof(cli_addr);
    
    while(1) {


        /* 6.  Why use while(1)? Based on the code below, what problems might occur if there are multiple simultaneous connections to handle?
        *   Using while(1) creates an infinite loop that ensures the server is continuously accepting and processing client connections until 
        the program is terminated. When it comes to multiple simultaneous connections, it is important to recall that the code processes connections 
        sequentially, so if multiple clients connect at once, the server can only handle a client once at a time, delaying other clients. 
        */
        
	char buffer[256];
        newsockfd = accept(sockfd, 
                    (struct sockaddr *) &cli_addr, 
                    &clilen);
	/* 7. Research how the command fork() works. How can it be applied here to better handle multiple connections?
         * The command fork() creates a new process, better known as a child, by duplicating a current process, 
         better known as a parent. To better handle multiple connections, the fork command child would handle the 
         connection or current client, while the parent listens for and accepts new connections. 
         */
        
	if (newsockfd < 0) 
             error("ERROR on accept");
	bzero(buffer,256);
        
	n = read(newsockfd,buffer,255);
        if (n < 0) 
            error("ERROR reading from socket");
        printf("Here is the message: %s\n",buffer);
        n = write(newsockfd,"I got your message",18);
        if (n < 0) 
            error("ERROR writing to socket");
        close(newsockfd);
    }
    close(sockfd);
    return 0; 
}
  
/* This program makes several system calls such as 'bind', and 'listen.' What exactly is a system call?
 * A system call is defined as an interface between a user-space program and the operating system kernel. 
 The system call allows programs to request specific services. An example of this would be “socket()” which, when called, creates a socket.
 */