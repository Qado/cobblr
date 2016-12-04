import SystemState
import Menu
import Screen
import Interrupt
import Timer
import GPIO
from evdev import InputDevice
import select
import time
import logging

def CheckScreenEvents():
  """Checks for any screen touches."""
  pygame = SystemState.pygame
  
  xpos = None
  ypos = None
  
  device = InputDevice("/dev/input/touchscreen")
  r,w,x = select.select([device], [], [], 0.2)
  
  try: 
    for event in device.read():
      if event.code == 53:
        xpos = event.value
      if event.code == 54:
        ypos = event.value
  except IOError:
    pass
   
  pos = (xpos, ypos)
  if xpos is not None and ypos is not None:
    time_delta = abs(time.time() - SystemState.screen_time)
    if time_delta > 0.15:
      SystemState.screen_time = time.time()
      Screen.ProcessScreenEvents(pos)

def CheckTimerEvents():
  Timer.CheckTimeOut()

def CheckGPIOEvents():
  """Checks for any GPIO button touches."""
  GPIO.ProcessGPIOEvents()

def CheckInterruptEvents():
  """Checks for any interrupts."""
  if SystemState.interrupt_queue.empty() is False:
    interrupt_args = SystemState.interrupt_queue.get()
    Interrupt.ProcessInterruptEvents(interrupt_args)

def CheckEvents():
  """Calls all three check events."""
  CheckScreenEvents()
  CheckGPIOEvents()
  CheckInterruptEvents()
  CheckTimerEvents()
