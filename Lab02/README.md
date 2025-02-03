# Lab 2

## Team Members
- Jadynne Zane
- Marco Ebeling

## Lab Question Answers

Answer for Question 1: 
The reliability of UDP decreased significantly when we added the 50% loss to our local environment. We sent over the number sequence 1-10 respectively but received the numbers “3, 6, 8, 9, 10,” which means half of the message was not received by the server.  UDP is known as a connectionless protocol and does not establish a reliable connection between the sender and receiver thus any packet loss that occurs during transmission due to network conditions is not recovered or retransmitted.


Answer for Question 2:
Even with the 50% loss to our local environment, TCP maintained reliable transmission of data, resulting in all messages being delivered, but in a delay. Unlike UDP, TCP is a connection-oriented protocol that ensures reliable transmission and communication between the sender and receiver. Thus, all data will be transmitted in the correct order with no loss even with bad network conditions.


Answer for Question 3:
The speed of the TCP response change decreased when in a 50% loss in our local environment. The time that was required to send and receive messages increased due to the process of retransmission and acknowledgments. TCP works by including packet retransmissions and flow control, which in hand introduces delays. So, for example, if a packet is lost, the sender of the original message must wait for a timeout or duplicate acknowledgment before retransmitting the data that is missing.
