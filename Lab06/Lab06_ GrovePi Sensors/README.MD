# Lab 6

## Team Members
- Jadynne Zane
- Marco Ebeling

# Lab Question Answers
Answer to Question 1:
$ git clone git@github.com:my-name/my-imaginary-repo.git
$ cd my-imaginary-repo
$ touch new_file.py
$ echo 'print("Hello World")' > new_file.py
$ git add new_file.py
$ git commit -m "Adding new file with hello world"
$ git push origin main

Answer to Question 2: 
For this lab, my partner and I developed the code on our local machine and then pushed/pulled the code from GitHub to the RPi. For this past lab, we had the wrong operating system flashed, but fixed that error. We feel that the method we used was efficient. Looking forward, we could be more efficient by familiarizing ourselves further with Git commands.

Answer to Question 3:
The library has a 60 ms delay. The Rpi uses I2C to communicate with Atmega328P. The delay is necessary communicating and processing via I2C takes a certain amount of time.s