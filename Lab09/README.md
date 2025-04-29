# Lab 3

## Team Members
Marco Ebeling
Jaydnne Zane

## Lab Question Answers

Question 1a: What type of authentication are we using here (currently)? Does it use any
keys?
Answer to Question 1a: We are using passwords for authenitification. No keys, just usernames and passwords

Question 1b: Both TLS (encryption) and crypto authentication use public-private key
pairs. For TLS encryption what keys are used when the client sends a message to the
server? For crypto authentication, explain how the server can verify a message is from a
given client?
Answer to Question 1b: The public key is used when the client sends a messages to the server for TLS. For crypto, the user signs with its private key. The server can verify this.

Question 2: Here we created a pair of asymmetric keys. What are their names? Which one
is the public key and which one is the private key?
Answer to question 2: We created server-key.pem (private) and server-cert.pem (public)

Question 3: What is a certificate authority (CA) for public keys? What kind of attack can a
CA prevent?
Answer to Question 3: CA issues certificates.This is to have a key associated with a user or server, which can be used for verification. This prevents a mean person from impersonating a verification service because that mean person won't have the CA certificate. This is man-in-the-middle