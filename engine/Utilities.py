import sys
import signal
import SystemState

def GracefulExit(signal, frame):
  SystemState.pygame.quit()
  sys.exit(0)

def Call(callback, callback_args=None):
  if callback_args is not None:
    if type(callback_args) is tuple:
      callback(*callback_args)
    elif type(callback_args) is dict:
      callback(**callback_args)
  else:
    callback()

