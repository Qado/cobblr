import SystemState
import RPi.GPIO
import logging

def ProcessGPIOEvents():
  for button in SystemState.gpio_interrupts:
    if (RPi.GPIO.input(button) == 0):
      message = gpio_buttons[button]
      logging.debug('gpio message', message)
      SystemState.interrupt_queue.put(message)


