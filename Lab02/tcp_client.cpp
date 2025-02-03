// Server side C/C++ program to demonstrate Socket programming 
// Here's some include statements that might be helpful for you
#include <string> 
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <sys/socket.h> 
#include <netdb.h>
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char const *argv[]) 
{ 
	// check to see if user input is valid
	char socket_read_buffer[1024];
	
	// TODO: Fill out the server ip and port
	std::string server_ip = "172.20.10.3";
	std::string server_port = "2560";

	int opt = 1;
	int client_fd = -1;

	// TODO: Create a TCP socket()
	client_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (client_fd < 0)
	{
		printf("Error- Socket creation failed");
		return -1;
	}
	// Enable reusing address and port
	if (setsockopt(client_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) { 
		return -1;
	}

	// Check if the client socket was set up properly
	if(client_fd == -1){
		printf("Error- Socket setup failed");
		return -1;
	}
	
	// Helping you out by pepping the struct for connecting to the server
	struct addrinfo hints;
	struct addrinfo *server_addr;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	getaddrinfo(server_ip.c_str(), server_port.c_str(), &hints, &server_addr);

	// TODO: Connect() to the server (hint: you'll need to use server_addr)
	if(connect(client_fd, server_addr->ai_addr, server_addr->ai_addrlen) < 0){ 
		printf("Error- Connection failed");
		return -1;
	}
	// TODO: Retreive user input
	cout << "Enter a user data: ";
	cin >> socket_read_buffer;
	// TODO: Send() the user input to the server
	n = write(client_fd, socket_read_buffer, strlen(socket_read_buffer));
	if (n<0) 
	{
		printf("Error- Writing to socket failed");
		return -1;
	}
	// TODO: Recieve any messages from the server and print it here. Don't forget to make sure the string is null terminated!
	char buffer_rec[1024];
	n = read(client_fd, buffer_rec, 1024);
	if (n<0) 
	{
		printf("Error- Reading from socket failed");
		return -1;
	}
	printf(buffer_rec, "\0");
	// TODO: Close() the socket
	close(client_fd);


	return 0; 
} 