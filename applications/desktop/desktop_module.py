from engine import TextWriter
from engine import SystemState
from engine import Menu
from engine import Timer
from engine import Screen
from engine import Events
import RPi.GPIO as GPIO
import serial
import sys
import os
import time


def Process():
  if SystemState.pressed_button == 'power':
    Menu.JumpTo('desktop', 2)
    TextWriter.Write(
      text="Shutdown Cobblr?",
      text_type='prompt',
      size=25,
      centered=True,
      permatext=True
      )
  elif SystemState.pressed_button == 'decline':
    Menu.Back()
  elif SystemState.pressed_button == 'accept':
    os.system('sudo init 0')
    SystemState.pygame.exit()
    sys.exit(0)
  else:
    Menu.JumpTo(SystemState.pressed_button, 1)
    
def Main():
  Screen.WakeScreen()
  Timer.SetTimeOut('sleep_screen', 7, Screen.SleepScreen, permanent=True)
  RefreshDesktop()

def RefreshDesktop():
  """Places the time and battery power on the screen.

  Args:
    None

  Return:
    None
  
  RefreshDesktop refreshes the clock, battery indicator, etc every 60 seconds.
  It does this by setting a permanent timeout that runs every 60 seconds. When
  it runs, RefreshScreen is called. When RefreshScreen is called, the desktop
  application's Main() function is called, which prints the new information
  on the screen.

  This is only called when the system is sitting on the desktop.
  """
  if SystemState.application == 'desktop':
    SystemState.screen.fill(SystemState.background_color)
    Menu.JumpTo('desktop', toggle=True, change_application=True)
