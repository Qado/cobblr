import TextWriter
import Utilities
import Menu
import logging


def ProcessInterruptEvents(interrupt_args):
  """Processes any interrupts sent out."""
  logging.debug('interrupt arguments %s', interrupt_args)
  callback = interrupt_args.get('callback', None)
  callback_args = interrupt_args.get('callback_args', None)
  Utilities.Call(callback, callback_args) 
