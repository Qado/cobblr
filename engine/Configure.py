#!/usr/bin/python

import yaml
import sys
import os
from engine import SystemState

#TODO: Figure out a way to make config files that allow users to configure apps.

def ConfigureApplication(application):
  if application == 'desktop':
    ConfigureDesktop()

def ConfigureDesktop():
  screen_modes = {}
  print "Configuring desktop"
  desktop_config = os.path.join(SystemState.cobblr_path,
      'applications/desktop/config/desktop.yaml')
  file_name = open(desktop_config, "r")
  file_content = yaml.load(file_name.read())
  icon_size = file_content['icon-size']
  screen_modes[1] = DesktopLayout(icon_size)
  screen_modes[2] = ConfirmLayout()
  file_content['screen-modes'] = screen_modes
  print "Generating new desktop config at", desktop_config
  config_object = open(desktop_config, 'w')
  yaml.dump(file_content, config_object)
  config_object.close()

def DesktopLayout(icon_size):
  desktop_layout = {}
  applications = list(SystemState.applications)
   
  if SystemState.install_application is not None: 
    applications.append(SystemState.install_application)
  elif SystemState.remove_application is not None:
    if SystemState.remove_application in applications:
      del applications[applications.index(SystemState.remove_application)] 
  del applications[applications.index('desktop')]

  # Setting up icon grid.
  xres = SystemState.resolution[0]
  yres = SystemState.resolution[1]

  # Grid maximum.
  row_max = xres/icon_size[0] - 2

  # Initial x and y positions.
  xpos_init = 1.60
  ypos_init = 2
  xpos = xpos_init
  ypos = ypos_init

  # Padding and iteration count.
  padding = 1.25
  count = 1

  # Checking for column limit.
  for application in applications:
    desktop_layout[application] = [xpos, ypos]
    
    # Laying out icons.
    if count % row_max != 0:
      xpos = xpos + padding
    else:
      xpos = xpos_init
      ypos = ypos + padding
    count += 1

    # Placing the reboot button.
  if xres > yres:
    desktop_layout['power'] = [8, 6]
  else:
    desktop_layout['power'] = [6, 8]

  return desktop_layout

def ConfirmLayout():
  confirm_layout = {}
  if SystemState.resolution[0] > SystemState.resolution[1]:
    confirm_layout['accept'] = [4, 3]
    confirm_layout['decline'] = [4, 6]
  else:
    confirm_layout['accept'] = [3, 4]
    confirm_layout['decline'] = [6, 4]
  return confirm_layout

if __name__ == '__main__':
  ConfigureDesktop()
