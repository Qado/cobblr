from engine import SystemState
from engine import Screen
from engine import TextWriter

def Back(change_application=False):
  """Moves backwards once in the history list.

  Args:
    change_application: determines if the application.

  Returns:
    None

  Back() sends the user to the previous application and/or screen mode.
  """
  SystemState.state_history_direction = -1
  if change_application is True:
    TextWriter.ClearPermatext()
    SystemState.screen.fill(SystemState.background_color)
    SystemState.ChangeState(SystemState.next_application, SystemState.next_screen_mode)
    SystemState.application_changed = True

def JumpTo(application=None, screen_mode=None, toggle=False,
        change_application=False, refresh_screen=True, store_history=True):
  """Switches the screen mode and/or application once called.

  Args:
    application: the application the function is jumping to.
    screen_mode: the screen_mode the function is jumping to.
    toggle: whether or not the change should be appended to the history list.
    change_application: variable for whether or not the application is being changed.
    refresh_screen: variable for whether or not the screen will be refreshed.

  Returns:
    None

  JumpTo() checks if the application or screen mode parameter is a
  Nonetype. If not, then set the next application and/or screen mode to their
  parameters accordingly. The toggle parameter determines if the change should
  be appended to the history list. This is good for buttons that are meant to 
  toggle values. The change_application parameter determines whether the
  function is going to change from its current running app to the next assigned 
  one. The refresh_screen parameter determines whether the screen should be
  updated.
  """
  if application is not None:
    SystemState.next_application = application
  if screen_mode is not None:
    SystemState.next_screen_mode = screen_mode
  if store_history is False:
    SystemState.store_history = False
  if toggle is not False:
    SystemState.state_history_direction = None
  else:
    SystemState.state_history_direction = 1
  
  if refresh_screen is False:
    SystemState.refresh_screen = False

  if change_application is True:
    SystemState.screen.fill(SystemState.background_color)
    SystemState.ChangeState(SystemState.next_application, SystemState.next_screen_mode)
    SystemState.application_changed = True
