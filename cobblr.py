#!/usr/bin/python
from engine import SystemState
from engine import Screen
from engine import config
from engine import TextWriter
from engine import Menu
from engine import Events
import sys
import os
import logging
import pygame
import time
import serial
import yaml
import importlib
import RPi.GPIO as GPIO
import threading
import signal
import pyaudio
import picamera


"""
Module: cobblr
Location: cobblr.py
"""

# Assigning Input and Outputs for PiTFT.
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')

# Setting Up GPIO Input and Output.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
pygame_clock = pygame.time.Clock()

def GracefulExit(signal, frame):
  logging.info('exiting Cobblr.')
  logging.debug('exiting signal: %s', signal)
  logging.debug('exiting frame: %s', frame)
  SystemState.pygame.quit()
  sys.exit(0)

signal.signal(signal.SIGINT, GracefulExit)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s', filename='cobblr.log', level=logging.DEBUG)
logger = logging.getLogger( __name__ )

def InitSystem():
  """Initilizes the entire system.
  
  Args:
    None

  Returns:
    None
  
  The Init() first initilizes pygame and sets the modes. Then, it loads
  applications defined in the cobblr.yaml configuration file. After that, it
  loads each module for each application and stores it in a list. If that
  module is present, it checks if there are functions in each module to be
  called. The functions are placed in each <application_name>_module.py file.

  The functions are:

    Init():
      Init sets up the environement or starts services necessary for the module
      to run.

    Process():
      Process runs when a button on the screen is pressed. It responds to the
      button press with an Screen.

    Main():
      Main runs after switching to an application. Any computation or animation
      being done belongs in the Main function. Main can hold a while loop, but
      the conditioning would have to be rigged like this:

         " while SystemState.application == (application_name): "

    Thread():
      Similar to Main, but get's called when Cobblr is initialized. Thread is
      a part of the module that get's spawned as a thread from within
      init. If there is a set of tasks that the module must run outside of the
      main thread, it is placed in the module's Thread function. 
  
  A module needs any of these to work correctly, depending on what it does.
  Init looks for these and either calls them, as is the case of Init and
  Thread, or uses them later based on some Screen. as is the case with Process
  and Screen.
  """
  logging.info('starting Cobblr.')
  # Initializing pygame and screen.
  pygame.init()
  pygame.mouse.set_visible(False)
  modes = pygame.display.list_modes(16)

  # Assigning variables used by other modules to SystemState
  SystemState.pyaudio = pyaudio.PyAudio()
  SystemState.pygame = pygame
  SystemState.screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 16)
  SystemState.cobblr_config = yaml.load(open("config/cobblr.yaml"))
  
  SystemState.gpio_interrupts = __FetchGPIOConfig()
  # Setup for storing application configs and modules.
  application_configs = {}
  application_modules = []
  applications = SystemState.cobblr_config["applications"]

  # Setup which application is the startup applicaton.
  startup_info = SystemState.cobblr_config["startup"]
  SystemState.startup_application = startup_info["application"]
  SystemState.startup_screen_mode = startup_info["screen_mode"]

  # Reading each application's config file.
  logging.info("reading application config files")
  
  for application in applications:
    application = str(application)
    application_dir = os.path.join("applications", application)
    application_config_dir = os.path.join(application_dir, "config")
    application_config  = os.path.join(application_config_dir, application + ".yaml")
    
    # Initializing the config.
    logging.debug('starting %s application.', application)
    config.Init(application_config)
    config_object = config.SystemConfig.applications[application]
    application_configs[application] = config_object
    application_module = config_object["module"]
    application_modules.append(application_module) 
  
  # Storing the application configs for use by other modules.
  SystemState.application_configs = application_configs

  # Initialize modules and pass them to the system state.
  application_modules = map(importlib.import_module, application_modules)
  SystemState.application_modules = dict(zip(applications, application_modules))

  # Initializing Thread and Init modules if available.
  logging.info('starting Init and Thread modules.')
  for application in SystemState.application_modules:
    current_application = config.SystemConfig.applications[application]
    init_settings = current_application["Init"]
    thread_settings = current_application["Thread"]

    if init_settings is True:
      SystemState.application = application
      logging.debug('starting Init() for %s', application)
      init = SystemState.application_modules[application]
      init.Init()

    if thread_settings is True:
      SystemState.application = application
      logging.debug('starting Thread() for %s', application)
      thread = SystemState.application_modules[application]
      module_thread = threading.Thread(target=thread.Thread)
      module_thread.start()
      SystemState.application = None
  
  # Refreshing the screen, setting up screen sleep, and changing to desktop.
  logging.info('loading splash')
  SystemState.BACKLIGHT.start(100)
  SystemState.backlight_on = True
  SystemState.screen.fill((255, 255, 255))
  SystemState.BACKLIGHT.start(100)
  cobblr_image = pygame.image.load("config/cobblr_splash_screen.png").convert()
 
  if SystemState.startup_screen_size[0] < SystemState.startup_screen_size[1]:
    SystemState.screen.blit(cobblr_image, (17, 120))
  else:
    SystemState.screen.blit(cobblr_image, (62, 90))

  SystemState.pygame.display.update()
  time.sleep(3)

  SystemState.screen.fill(SystemState.background_color)
  # Jump to the application and screen mode specifed in cobblr.yaml.
  Menu.JumpTo(
      application=SystemState.startup_application,
      screen_mode=SystemState.startup_screen_mode, 
      change_application=True
  )


def __FetchGPIOConfig():
  gpio_config = yaml.load(open("config/gpio.yaml"))
  gpio_interrupts = gpio_config["gpio_interrupts"]
  return gpio_interrupts


def RunCobblr():
  """Starts the Cobblr main thread.

  Args:
    None

  Returns:
    None

  RunCobblr is the main thread that starts up cobblr and it's applications.
  """
  InitSystem()
  
  # Cobblr's main loop.
  logging.info('start of Cobblr main loop')
  while(True):
    #pygame_clock.tick(60)
    Events.CheckEvents()
  logging.critical('Cobblr main loop exited!')
  

if __name__ == '__main__':
  RunCobblr()
