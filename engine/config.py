#!/usr/bin/python
import SystemState
import yaml
import sys #can remove after testing
import os
import logging


"""Module: config"""

class SystemConfig(object):
  applications = {}

def Init(config_file):
  """Initializes configurations for each application.

  Args: 
    config_file: a yaml file that contains system configuration information.

  Returns:
    None

  Init() accepts a yaml configuration file and uses it to calculate button
  positions, modules to be loaded, and the location of each button. The buttons
  are named after their 'png' file, so the names of each button in the config
  translates back into the png.

  The configuration is then stored in the SystemConfig class. THe class is then
  read each time an action is performed on the screen or buttons.
  """
  # Reading config file and turing it into a yaml object.
  file_name = open(config_file, "r+")
  logging.debug('reading config.yaml file at %s', config_file)
  file_content = yaml.load(file_name.read())

  # Fetching data to create application config info.
  application = str(file_content['application'])
  icon_directory = os.path.join('applications', application, 'icons')
  icon_size = file_content['icon-size']
  icon_x = icon_size[0]
  icon_y = icon_size[1]
  screen_size = file_content['screen-size']
  screen_modes = file_content['screen-modes']

  if SystemState.startup_application == 'desktop':
      SystemState.startup_screen_size = screen_size

  # Checking for module settings
  init_settings = file_content.get('Init')
  process_settings = file_content.get('Process')
  thread_settings = file_content.get('Thread')
  main_settings = file_content.get('Main')
  module_settings = file_content.get('module-settings')

  # Adding properties to SystemConfig for the application.
  SystemConfig.applications[application] = {}
  current_app = SystemConfig.applications[application]
  current_app["modes"] = {}
  module_name = "applications." + application + "." + application + "_module"
  current_app["module"] = module_name
  current_app["Init"] = init_settings
  current_app["Process"] = process_settings
  current_app["Thread"] = thread_settings
  current_app["Main"] = main_settings
  current_app["module-settings"] = module_settings

  # Calculating icon position and adding to system config.
  for mode in screen_modes:
    current_app["modes"][mode] = {}
    buttons = screen_modes[mode]
    for button in buttons:
      current_button = buttons[button]
      xmax = current_button[0] * icon_x
      ymax = current_button[1] * icon_y
      xmin = xmax - icon_x
      ymin = ymax - icon_y
      fname = os.path.join(icon_directory, str(button) + ".png")
      mode_data = {
          'xmax': xmax, 
          'ymax': ymax, 
          'xmin': xmin, 
          'ymin': ymin, 
          'file': fname
      }
      current_app["modes"][mode][button] = mode_data
