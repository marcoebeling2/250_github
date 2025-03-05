# Lab 5

## Team Members
- Jadynne Zane
- Marco Ebeling

## Lab Question Answers

Answer for Question 1: 

dBm is a unit of measurement for the strength of the signal. It takes in a value in mW and converts it to a log scale via:
dBm = 10 * log10(mW)

Answer for Question 2:
The different OS have different methods used to get signal strength. They return different values and formats, so we need to have specifics regex for each.

Answer for Question 3:
it runs a shell command and retrieves the output of that command.

Answer for Question 4:
it is matching a regex for the output of the previously run shell command.

Answer for Question 5:
signal quality is a percentage of maximal strength, which is -100 dbm, so we need to conver it.

Answer for Question 6:
standard deviation is the measure of variance that an average sample has from the mean. This can show the stability of the wifi signal.

Answer for Question 7: 
a dataframe is basically the python version of an excel spreadsheet. It stores data in a 2D tabular format. It is useful because there are easy built in function to index and manipulate the data in whatever way you want.

Answer for Question 8:
error bars are important because they give us key insight into the variance of the data we collected. Plotting this shows the stability of the singal.

Answer for Question 9:
as I got further away, the signal got weaker and less stable. The best wifi is in my bedroom and living room!

Questions for Part 2:
Answer for Question 1:
How does distance affect TCP and UDP throughput? Distance thoroughly affects TCP and UDP throughput. When the distance form the WiFi access point increases, the signal strength decreases and the error rates increase. TCP throughput drops due to the congestion control decreases due to lost packets, while UDP sees dropped packets without decreasing its sending rate significantly. 

Answer for Questino 2:
At what distance does significant packet loss occur for UDP? For UDP, significant packet loss occurs when the WiFi signal falls below -70 dBm which happens commonly around 50-100 ft. However, exact distance varies based on power levels, obstacles, and interference. 

Answer for Question 3:
Why does UDP experience more packet loss than TCP? UDP does not contain congestion control and does not automatically retransmit lost packets. UDP can overwhelm the network or receive buffers which in hand result in more drops than TCP, which adjusts its rate in order to prevent ongoing loss. 

Answer for Question 4:
What happens if we increase the UDP bandwidth (-b 100M)? Packet loss will surge if we increase the UDP bandwidth (-b 100M). The sender keeps transmitting at a specified rate, so the excess packets get dropped 

Answer for Question 5:
Would performance be different on 5 GHz Wi-Fi vs. 2.4 GHz? Yes, 2.4 GHz often can provide a better range but experiences more interference and lower peak speeds, while 5 GHz offers higher potential throughput but has a shorter effective range and is worse at wall penetration. 