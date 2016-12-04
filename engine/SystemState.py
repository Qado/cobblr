import SystemState
import pwd
import grp
import picamera
import logging 
import pyaudio
import Queue
import random
import Screen
import RPi.GPIO
import inspect

RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(12, RPi.GPIO.OUT)

"""Container for the current state of the system and applications."""
application = None  # Specifying what application the system is running
screen_mode = None  # Specifying what mode the application should start in
button_action = False # Setting up whether a button was pressed or not.
uid = pwd.getpwnam("pi").pw_uid
gid = grp.getgrnam("pi").gr_gid
rgb = bytearray(320 * 240 * 3)
store_history = True
state_history = []
state_history_direction = None
interrupt_queue = Queue.Queue()
background_color = random.randrange(0, 65535)
refresh_screen = True
battery_power = None
pressed_buttons = ''
pressed_button = None
link_destination = None
screen_on = True
screen_time = 0
previous_xpos = None
previous_ypos = None
permatext = []
backlight_on = True
startup_screen_size = 0
application_changed = False
BACKLIGHT = RPi.GPIO.PWM(12, 50)

def ChangeState(application, screen_mode):
  """Changes the running application on the system.

  Args:
    application (str): the name of the application you'd like to switch to.
    screen_mode (int): The number of the mode the application should switch to.
 
  Returns:
    None.
 
  ChangeState changes the state, screen mode, or state and screen mode of an
  application. It also stores the last application's state and screen mode. It
  does this by changing the properties in SystemState. These can be modified
  and retrieved as class methods.

    SystemState.<thing_in_there>
  
  As a convenience, it keeps the attributes of any application that had it's
  screen mode changed. That way, applications can be interrupted and return to
  their previous running states in the <application_name>_lastattr attribute in
  SystemState. If this is going to be used, it's best to fetch it by using
  getattr(). For example:

    <app>_lastattr = getattr(SystemState, <app>_lastattr, None)

  Then proceeding accordingly.
  """
  # Preserving previous screen mode and app
  SystemState.previous_application = SystemState.application
  SystemState.previous_screen_mode = SystemState.screen_mode
 
  # If something other than a button requests a state change, do it.
  SystemState.next_application = application
  SystemState.next_screen_mode = screen_mode
  
  if SystemState.store_history is True:
    if SystemState.state_history_direction == -1: #remove
      if len(SystemState.state_history) > 1:
        SystemState.state_history = SystemState.state_history[:-1]
      else:
        SystemState.state_history = [SystemState.state_history[0]]
      SystemState.next_application = SystemState.state_history[-1][0]
      SystemState.next_screen_mode = SystemState.state_history[-1][1]
    elif SystemState.state_history_direction == None: #toggle
      SystemState.state_history = SystemState.state_history[:-1]
      previous_state = (SystemState.next_application, SystemState.next_screen_mode)
      SystemState.state_history.append(previous_state)
      SystemState.next_application = SystemState.state_history[-1][0]
      SystemState.next_screen_mode = SystemState.state_history[-1][1]
    elif SystemState.state_history_direction == 1: #add
      previous_state = (SystemState.next_application, SystemState.next_screen_mode)
      SystemState.state_history.append(previous_state)
      SystemState.next_application = application
      SystemState.next_screen_mode = screen_mode
  else:
    SystemState.store_history = True
  
  logging.debug("AppHistory: %s", SystemState.state_history)
  SystemState.state_history_direction = None

  # Changing the state to the new state. 
  SystemState.application = SystemState.next_application
  SystemState.screen_mode = SystemState.next_screen_mode
  
   # Fetching new modes.
  SystemState.application_config = SystemState.application_configs[SystemState.application]
  SystemState.application_modes = SystemState.application_config["modes"]
  SystemState.application_module = SystemState.application_modules[SystemState.application]
  SystemState.mode_buttons = SystemState.application_modes[SystemState.screen_mode]

  # To avoid loading icons every time the application is switched.
  logging.info("changing application from %s to %s", SystemState.previous_application, application)
  SystemState.pressed_button = ''
  Screen.LoadIcons()

  # Don't refresh the screen if we don't wanna!
  if SystemState.refresh_screen == True: 
    Screen.RefreshScreen()
  else: 
    SystemState.refresh_screen = True
  
  SystemState.application_changed = False
  # Check for a refresh function and call it.
  current_application = SystemState.application_configs[SystemState.application]
  main_settings = current_application["Main"]

  # Checking to make sure we aren't already in the module's Main().
  stack_modules  = [i[3] for i in inspect.stack()]
  if 'Main' not in stack_modules:
    if main_settings is True:
      module = SystemState.application_modules[SystemState.application]
      module.Main()
      SystemState.screen.fill(SystemState.background_color)
      Screen.RefreshScreen()

