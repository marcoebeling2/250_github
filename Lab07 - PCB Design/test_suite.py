import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#using physical pin 11 to blink an LED
GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# by taking readings and printing them out, find
# appropriate threshold levels and set them 
# accordingly. Then, use them to determine
# when it is light or dark, quiet or loud.
lux_treshold=487  # change this value
sound_treshold=450 # change this value

# light sensor channel
light_adc = 0
# sound sensor channel
sound_adc = 1


while True: 
  time.sleep(0.5) 

  #Following commands control the state of the output
  #GPIO.output(pin, GPIO.HIGH)
  #GPIO.output(pin, GPIO.LOW)

  # get reading from adc 
  # mcp.read_adc(adc_channel)
  

  # Blink led in 5 times with 500ms on/off intervals
  for _ in range(5):
      GPIO.output(11, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(11, GPIO.LOW)
      time.sleep(0.5)
  
  
  # read lead sensor and print out hte value
  start_time = time.time() # get start time to measure 5 sec span
  while time.time() - start_time < 5:
      light_val = mcp.read_adc(light_adc)  
      if light_val > lux_treshold: # check if brightness is bigger than the threshold
          status = "bright"
      else:
          status = "dark"
      print("Light Sensor: {} - {}".format(light_val, status))
      time.sleep(0.1)
  
   # Blink led in 4 times with 200ms on/off intervals
  for _ in range(4):
      GPIO.output(11, GPIO.HIGH)
      time.sleep(0.2)
      GPIO.output(11, GPIO.LOW)
      time.sleep(0.2)
  
  # read sound sensor for 5 seconds and print out the value
  start_time = time.time() # start time to calculate when 5 seconds is up
  led_on_until = 0  # Timestamp until which the LED should remain on
  while time.time() - start_time < 5:
      sound_val = mcp.read_adc(sound_adc)  # read sound adc val
      print("Sound Sensor: {}".format(sound_val)) # print the value
      if sound_val > sound_treshold: # if the threshold is exceeded
          # get the start time of the led on period
          start_time = time.time()
          # calculate the end time
          end_time = start_time + 0.1
      # keep the LED on if not end time yet
      if time.time() < end_time:
          GPIO.output(11, GPIO.HIGH)
      else:
          GPIO.output(11, GPIO.LOW)
      time.sleep(0.1)
    
  