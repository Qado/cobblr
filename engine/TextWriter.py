import SystemState
import logging

def Write(**kwargs):
  logging.info('writing text to screen.')
  text = kwargs.get('text', 'NO TEXT')
  text = str(text)
  position = kwargs.get('position', (10, 80))
  color = kwargs.get('color', (255, 255, 255))
  size = kwargs.get('size', 15)
  centered = kwargs.get('centered', False)
  font = kwargs.get('font', 'Arial')
  text_type = kwargs.get('text_type', None)
  permatext = kwargs.get('permatext', False)

  # Checking and setting permanent text,

  if permatext is True:
    logging.debug('setting text "%s" to permanent', text)
    SystemState.permatext.append(kwargs)

  # Sets up default text types in the UI
  if text_type is not None:
    if text_type == 'message':
      position = (10, 80) 
      size = 30
    if text_type == 'subtext':
      position = (10, 120)
      size = 20
    if text_type == 'top':
      position = (10, 10)
      size = 30
    if text_type == 'system':
      position = (20, 10)
      size = 40
    if text_type == 'clock':
      position = (100, 5)
      size = 15
    if text_type == 'battery':
      position = (200, 5)
      size = 15
    if text_type == 'settings':
      pass
    if text_type == 'prompt':
      position = (160, 50)
      centered = True

  pygame = SystemState.pygame # usually SystemState
  screen = SystemState.screen
  text_font = pygame.font.SysFont(font, size)

  if centered == True:
    text_width = text_font.size(text)[0]
    x = position[0] - (text_width/2)
    position = (x, position[1])

  text = text_font.render(text, 1, color)
  screen.blit(text, position)

def ClearPermatext():
  logging.debug('clearing permatext "%s"', SystemState.permatext)
  SystemState.permatext = []

