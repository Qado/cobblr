import SystemState
import Utilities
import time
import logging

class TimeOuts(object):
  pass

SystemState.TimeOuts = TimeOuts

def SetTimeOut(timeout_name, time_span, callback, callback_args=None, permanent=False):
  """Sets timeouts for system events.

  Args:
    timeout_name (str): The name of the timeout used in the TimeOuts class.
    time_span (int): The amount of time (secs) until timeout is called.
    callback (func): The function called when the timeout time has elapsed.
    callback_args (dict,tuple): Arguments for the callback function above.
    permanent (bool): Sets whether TimeOut variable is deleted after called.

  Returns:
    None.

  SetTimeOut sets a timeout as a class variable in the TimeOuts class.
  CheckTimeOut then checks the TimeOuts class for it's class variables. When
  one is found, it then calls the callback function and deletes the class
  variable.

  It sets the variable with:

      <timeout_name> = (<time_span>, <timeout_time>, <callback>, <permanent>)

  Where <timeout_time> is the unix time (int) plus the number of seconds in the
  <time_span>. All system related timeouts are set here.
  """
  logging.debug("setting timeout %s", timeout_name)
  timeout_time = int(time.time()) + time_span
  timeout_application = SystemState.application
  setattr(SystemState.TimeOuts, timeout_name, (time_span, timeout_time,
      timeout_application, callback, callback_args, permanent))

def DeleteTimeOut(timeout_name):
  """Deletes timeouts.

  Args:
    timeout_name(str): The name of the timeout to be deleted.

  Returns:
    None.

  A convenient way to delete timeouts that you no longer need.
  """
  if hasattr(SystemState.TimeOuts, timeout_name):
    delattr(SystemState.TimeOuts, timeout_name)

def CheckTimeOut():
  """Check's the TimeOuts class for timeouts.

  Args:
    None

  Returns:
    None

  CheckTimeOut looks for timeouts set by SetTimeout. SetTimeout sets them as
  class variables. When CheckTimeOut finds one, it compares the current time to
  the time set by the timeout. If it's over, matches, or is beyond the timeout
  time by the amount of time set in the timeout (in seconds), it calls the
  callback function assigned to that timeout.

  If the timeout is permanent, it is kept. If not, it's deleted.
  """
  for timeout_name, timeout_data in SystemState.TimeOuts.__dict__.items():
    if timeout_name.find('__') != 0:
      # Setting up timeout variables.
      time_span = timeout_data[0]
      timeout_time = timeout_data[1]
      timeout_application = timeout_data[2]
      callback = timeout_data[3]
      callback_args = timeout_data[4]
      permanent = timeout_data[5]
      now_time = int(time.time())

      if timeout_application == SystemState.application:
        # Checking timeout object to see what it contains.
        if now_time - timeout_time >= 0:
          Utilities.Call(callback, callback_args)
          logging.debug("timeout %s has expired", timeout_name)

          # Deleting the stale timeout and resetting it if permanent is True.
          if hasattr(SystemState.TimeOuts, timeout_name):
            delattr(SystemState.TimeOuts, timeout_name)
          if permanent is True:
            SetTimeOut(timeout_name, time_span, callback, callback_args, permanent=True)
