# Import required libraries
import sys
import RPi.GPIO as GPIO
import time 
from numclass import CounterNumber
#import variable commandcount from main.py
######


global counter

#def set_counter(newCounter):
# counter = newCounter

'''
class Number():
    def init(self, count = 0):
        self.count = count

    #getter method
    def get_count(self):
        return self.count

    #setter method
    def set_count(self, x):
        self.count = x
'''
######
#toDisplay="12.28" # bot data here (commandcount)
def setup():
 delay = 1#.001 # delay between digits refresh

# --------------------------------------------------------------------
# PINS MAPPING AND SETUP
# selDigit activates the 4 digits to be showed (1 is active, 0 is unactive)
# display_list maps segments to be activated to display a specific number inside the digit
# digitDP activates Dot led
# --------------------------------------------------------------------

 selDigit = [14,15,18,23]
# Digits:   1, 2, 3, 4

 display_list = [24,25,8,7,1,12,16] # define GPIO ports to use
#disp.List ref: A ,B ,C,D,E,F ,G

 digitDP = 20
#DOT = GPIO 20

# Use BCM GPIO references instead of physical pin numbers
 GPIO.setmode(GPIO.BCM)

# Set all pins as output
 GPIO.setwarnings(False)
 for pin in display_list:
   GPIO.setup(pin,GPIO.OUT) # setting pins for segments
 for pin in selDigit:
   GPIO.setup(pin,GPIO.OUT) # setting pins for digit selector
 GPIO.setup(digitDP,GPIO.OUT) # setting dot pin
 GPIO.setwarnings(True)

# DIGIT map as array of array ,
#so that arrSeg[0] shows 0, arrSeg[1] shows 1, etc
 arrSeg = [[0,0,0,0,0,0,1],\
          [1,0,0,1,1,1,1],\
          [0,0,1,0,0,1,0],\
          [0,0,0,0,1,1,0],\
          [1,0,0,1,1,0,0],\
          [0,1,0,0,1,0,0],\
          [0,1,0,0,0,0,0],\
          [0,0,0,1,1,1,1],\
          [0,0,0,0,0,0,0],\
          [0,0,0,0,1,0,0]]

 GPIO.output(digitDP,0) # DOT pin

 return delay, selDigit, display_list, digitDP, arrSeg

# --------------------------------------------------------------------
# MAIN FUNCTIONS
# splitToDisplay(string) split a string containing numbers and dots in
#   an array to be showed
# showDisplay(array) activates DIGITS according to array. An array
#   element to space means digit deactivation
# --------------------------------------------------------------------

def showDisplay(digit, delay, selDigit, display_list, digitDP, arrSeg):
 for i in range(0, 4): #loop on 4 digits selectors (from 0 to 3 included)
  sel = [0,0,0,0]
  sel[i] = 1
  GPIO.output(selDigit, sel) # activates selected digit
  if digit[i].replace(".", "") == " ": # space disables digit
   GPIO.output(display_list,0)
   continue
  numDisplay = int(digit[i].replace(".", ""))
  GPIO.output(display_list, arrSeg[numDisplay]) # segments are activated according to digit mapping
  #GPIO.output(display_list, arrSeg[i])
  if digit[i].count(".") == 1:
   GPIO.output(digitDP,0)
  else:
   GPIO.output(digitDP,1)
   time.sleep(delay)

def splitToDisplay (toDisplay, delay, selDigit, display_list, digitDP, arrSeg): # splits string to digits to display
 arrToDisplay=list(toDisplay)
 for i in range(len(arrToDisplay)):
  if arrToDisplay[i] == ".": arrToDisplay[(i-1)] = arrToDisplay[(i-1)] + arrToDisplay[i] # dots are concatenated to previous array element
 while "." in arrToDisplay: arrToDisplay.remove(".") # array items containing dot char alone are removed
 return arrToDisplay

# --------------------------------------------------------------------
# MAIN LOOP
# persistence of vision principle requires that digits are powered
#   on and off at a specific speed. So main loop continuously calls
#   showDisplay function in an infinite loop to let it appear as
#   stable numbers display
# --------------------------------------------------------------------
#count = Number()
#count.init()
stupidlist = []
stupidlist.append("0")
#try:

# while True:
def tick(counter, delay, selDigit, display_list, digitDP, arrSeg):
 try:
  c = 0
  #number = count.get_count()
  number = counter.count
  sNumber = str(number)
  for element in range (0, len(sNumber)):
    c += 1
  while (c < 4):
    sNumber = " " + sNumber
    c+=1
  print(sNumber)
  showDisplay(splitToDisplay(sNumber, delay, selDigit, display_list, digitDP, arrSeg), delay, selDigit, display_list, digitDP, arrSeg)
 except KeyboardInterrupt:
   print("interrupted!")
   GPIO.cleanup()
   sys.exit()

#try:
#  test()
#except KeyboardInterrupt:
# print('interrupted!')
# GPIO.cleanup()
#sys.exit()

