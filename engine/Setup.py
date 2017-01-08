#!/usr/bin/python

from engine import SystemState
from engine import Configure
import sys
import os
import logging
import yaml


def InstallApplication(application):
  """Installs an application.

  Pulls an application from the repo. Then installs it.

  Args:
    application: The name of the application to be installed.

  Returns:
    None.

  It then cleans up it's mess.
  """
  # Cloning repo.
  # TODO: Make this configuarble.
  if application == 'cobblr':
    __InstallCobblr()
  else:
    __InstallApplication(application)


def RemoveApplication(application):
  """Removes an application.

  Args:
    application: the name of the application to be removed.

  Returns:
    None.

  Removes whatever application located in the the cobblr_path.
  """
  print "Removing ", application
  os.chdir(SystemState.cobblr_path)
  application = application.split('-')[-1]

  # Setting up paths.
  applications_path = os.path.join(SystemState.cobblr_path, 'applications')
  application_path = os.path.join(applications_path, application)
  icons_path = os.path.join(applications_path, 'desktop/icons')

  application_icon = application + '.png'
  icon_path = os.path.join(icons_path, application_icon)

  # Removing icon.
  print "Removing desktop icon"
  msg = 'Removing ' +  application + ' icon.'
  logging.info(msg)
  remove_icon = 'rm ' + icon_path
  os.system(remove_icon)

  # Removing path.
  print "Removing path"
  msg = 'Removing ' + application + ' directory'
  logging.info(msg)
  remove_application = 'rm -rf ' + application_path
  os.system(remove_application)

  msg = 'Finished removing ' + application + '.'
  logging.info(msg)
  Configure.ConfigureDesktop()


def __InstallCobblr():
  logging.info('Installing Cobblr. Please wait...')
  # Setting up variables.
  cobblr_executable = os.path.join(SystemState.cobblr_path, 'cobblr.py')
  cobblr_symlink = '/usr/local/bin/cobblr'
  current_path = os.getcwd()

  # Removing old install.
  print "Removing old Cobblr install at " + SystemState.cobblr_path
  remove_cobblr = 'rm -rf ' + SystemState.cobblr_path
  remove_symlink = 'rm -rf ' + cobblr_symlink
  os.system(remove_cobblr)
  os.system(remove_symlink)

  # Performing install.
  print "Installing Cobblr to " + SystemState.cobblr_path
  copy_cobblr = 'cp -r ' + current_path + ' ' + SystemState.cobblr_path
  os.system(copy_cobblr)
  os.symlink(cobblr_executable, '/usr/local/bin/cobblr')
  logging.info('Finished installing Cobblr')

def __InstallApplication(application):
  print "Cloning repo for ", application
  clone_repo = 'git clone http://github.com/TheQYD/' + application
  os.system(clone_repo)
  msg = 'Cloned', application
  logging.info(msg)

  # Collecting application info.
  os.chdir(application)
  application_content = os.listdir('.')
  for file_name in application_content:
    if 'module' in file_name:
      module_name = file_name.split('_')[0]
      icon_name = module_name + '.png'

      # Checking for dependencies.
      try:
        deps = yaml.load(open('deps.yaml'))
      except:
        deps = None

  # Finding module files.
  module_files = [i for i in application_content if '.png' not in i]
  if deps is not None:
    install_deps = 'apt-get install -y ' + deps
  try:
    print "Installing dependencies. Please wait..."
    os.system(install_deps)
  except:
    pass

  # Putting it all together.
  __InstallModule(SystemState.cobblr_path, module_name, module_files)
  __InstallDesktopIcon(SystemState.cobblr_path, icon_name)
  __DeleteClone(application)
  Configure.ConfigureDesktop()


def __InstallDesktopIcon(cobblr_path, icon_name):
  print "Installing applications"
  icon_path = os.path.join(cobblr_path, 'applications/desktop/icons')
  if os.path.exists(icon_path) is False:
    os.makedirs(icon_path)

  # Copying icon.
  icon_dest = os.path.join(icon_path, icon_name)
  copy_icon = 'cp -r ' + icon_name + ' ' + icon_dest
  os.system(copy_icon)
  msg = 'Installed', icon_name
  logging.info(msg)


def __InstallModule(cobblr_path, module_name, module_files):
  install_path = os.path.join(cobblr_path, 'applications')
  module_path = os.path.join(install_path, module_name)

  print "Installing module application module."
  # Making application path if it doesn't exist.
  if os.path.exists(module_path) is False:
    os.makedirs(module_path)

  # Moving module to application path.
  for module_file in module_files:
    module_dest = os.path.join(module_path, module_file)
    copy_module = 'cp -r ' + module_file + ' ' + module_dest
    os.system(copy_module)

  # Creating init file.
  init_file = os.path.join(module_path, '__init__.py')
  open(init_file, 'w').close()

  msg = 'Installed', module_name
  logging.info(msg)


def __DeleteClone(application):
  os.chdir(SystemState.cobblr_path)
  print "Deleting clone ", application
  delete_clone = 'rm -rf ' + application
  os.system(delete_clone)
  print "Clone deleted."
