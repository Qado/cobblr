import SystemState
import TextWriter
import time
import logging


def ProcessScreenEvents(pos):
  """Processes each touch against the screen.

  Args:
    pos: position returned by pygame.mouse.get_pos().

  Returns:
    None

  ProcessScreenEvents() checks the positions returned by pygame after it gets a touch
  event. It checks for the button positions calculated from the values in the
  application's config file. If the button is pressed, it calls the current
  running application's Process() function, which returns the system state.

  After that, it checks for state changes then refreshes the screen.
  """
  # Fetching the system state.
  mode_buttons = SystemState.mode_buttons
  application_module = SystemState.application_module

  # Resets the backlight if it's off.
  if SystemState.backlight_on == False:
    logging.debug('turning on screen backlight')
    WakeScreen()
    return None
  
  # Fetching pressed button.
  for key, value in mode_buttons.iteritems():
    xpos = pos[0] # Touched x position.
    ypos = pos[1] # Touched y position.
    xmin = value['xmin']
    ymin = value['ymin']
    xmax = value['xmax']
    ymax = value['ymax']
    
    logging.debug('screen was touched at %d,%d', xpos, ypos)
    # Checking which area of the screen corresponds to a touched button.
    if xpos >= xmin and xpos <= xmax and ypos >= ymin and ypos <= ymax:
      SystemState.permatext = []
      SystemState.button_action = True
      SystemState.screen.fill(SystemState.background_color)
      SystemState.pressed_button = key
      logging.debug('the %s button was pressed.', key)
      application_module.Process()
      application = SystemState.next_application
      screen_mode = SystemState.next_screen_mode
      logging.debug('next application: %s', application)
      logging.debug('next screen mode: %s', screen_mode)
      if SystemState.application_changed is False:
        SystemState.ChangeState(application, screen_mode)
      SystemState.pressed_button = ''
  SystemState.application_changed = False
  SystemState.pygame.event.clear()
  SystemState.last_event_time = int(time.time())

def LoadIcons():
  """Loads the icons in the application's 'icons' directory.
  
  Args:
    None

  Returns:
    None
  
  LoadIcons() fetches all of the icons for the application defined in it's
  configuration (<app_name>.yaml>). This sets them to the current running set
  of active_buttons in SystemState. These are the buttons that are checked when
  Action looks for which buttons may have been pressed.
  
  Actions tied to these buttons are processed in the applications
  <app>_module.py.
  
  """
  logging.debug('loading icons for %s', SystemState.application)
  application_modes = SystemState.application_modes
  SystemState.active_buttons = {}
  pygame = SystemState.pygame

  for mode in application_modes:
    mode_data = application_modes[mode]
    mode_buttons = {}
    for button in mode_data:
      try:
        icon_file = pygame.image.load(mode_data[button]["file"])
      except:
        icon_file = mode_data[button]["file"]
      mode_data[button]["file"] = icon_file
      mode_buttons[button] = mode_data[button]
      SystemState.active_buttons[mode] = mode_buttons


def RefreshScreen(image=None, wx=None, wy=None):
  """Clearing and placing buttons on the screen.

  Args:
    image: the image file that is being placed.
    wx: the x-position of the image file.
    wy: the y-position of the image file.

  Returns:
    None

  RefreshScreen checks the position of the buttons of the current running
  application and places them accoridingly.
  """
  logging.info('refreshing screen for %s', SystemState.application)
  screen = SystemState.screen
  screen_mode = SystemState.screen_mode
  mode_buttons = SystemState.mode_buttons
  active_buttons = SystemState.active_buttons[screen_mode]
  
  # Loading images to the screen (used to show images for the camera).
  if image is not None:
    screen.blit(image, (wx, wy))
  # Loading active buttons for the current application and mode.
  for mode_button in mode_buttons:
    button = active_buttons[mode_button]
    xmin = button["xmin"]
    xmax = button["xmax"]
    ymin = button["ymin"]
    ymax = button["ymax"]
    icon = button["file"]
    screen.blit(icon, (xmin, ymin))
  
  # Chceking if text is to be kept between button presses.
  logging.debug('writing to screen for %s', SystemState.application)
  for text in SystemState.permatext:
    text['permatext'] = False
    TextWriter.Write(**text)
  SystemState.pressed_button = None
  SystemState.pygame.display.update() # updating entire display.


def SleepScreen():
  """A function for the PiTFT's backlight.

  Args:
    None

  Returns:
    None
  
  SleepScreen is called when the timeout for screen sleep is called. When the
  screen is pressed, the backlight cuts back on and renews the timeout.
  """
  logging.info('turn off screen backlight during %s', SystemState.application)
  if SystemState.backlight_on == True:
    SystemState.BACKLIGHT.ChangeDutyCycle(0)
    SystemState.backlight_on = False

def WakeScreen():
  """A function to wake PiTFT's backlight.

  Args:
    None

  Returns:
    None
  
  SleepScreen is called when the timeout for screen sleep is called. When the
  screen is pressed, the backlight cuts back on and renews the timeout.
  """
  logging.info('turn on screen backlight during %s', SystemState.application)
  if SystemState.backlight_on == False:
    SystemState.BACKLIGHT.ChangeDutyCycle(100)
    SystemState.backlight_on = True
