import sys
sys.path.append('~/Dexter/GrovePi/Software/Python')
import time
import grovepi
from grove_rgb_lcd import *

# Grove Ultrasonic Ranger connectd to digital port 2
ultrasonic_ranger = 2
# potentiometer connected to analog port A0 as input
potentiometer = 0
grovepi.pinMode(potentiometer,"INPUT")

# clear lcd screen  before starting main loop
setText("")

while True:
  try:
    # TODO:read distance value from Ultrasonic Ranger and print distance on LCD
    # read the distance from the ultrasonic senser
    distance = grovepi.ultrasonicRead(ultrasonic_ranger)

    # TODO: read threshold from potentiometer
    # read value from potentiometer
    threshold_analog = grovepi.analogRead(potentiometer)
    # convert the analog value to threshold value
    max_dist = 400 # 400 cm max
    threshold = int(threshold_analog/1023 * max_dist)

    
    # TODO: format LCD text according to threshhold
    # fromat threshold appropriately
    lcd_string = f"{threshold:4}cm"
    # check if the distance is less than threshold
    if distance < threshold:
      lcd_text += "OBJ PRES" # change string if color is present
      # change color to red
      setRGB(255,0,0)
    else: # if the object is not in range...
        # keep color green
        setRGB(0,255,0)

    # Display on LCD
    setText_norefresh(f"{lcd_text}\n{distance:4}cm")
  
    
  except IOError:
    print("Error")