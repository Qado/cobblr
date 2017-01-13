# Cobblr
a Python framework used to make apps for the Raspberry Pi.   
![(Cobblr Images](photos/cobblr_collage.png?raw=true "Cobblr")

# Details
Cobblr is basically a state manager that allows Python modules to run code when a button on the screen is pressed. To keep
things familiar, I call these apps. Each app can be downloaded from Github using the Cobblr.

# Parts Required
All that's absolutely required to use Cobblr is:
- 1 [Raspberry Pi](https://www.adafruit.com/products/3055)
- 1 [Adafruit PiTFT](https://www.adafruit.com/products/2423)

The Raspberry Pi requires 

All other components are optional, though you'll probably want them to make things of your own. 

For example, to use cobblr-phone, you'll need:

- 1 [Adafruit Fona](https://www.adafruit.com/products/1963)

If the phone needed to be portable, you'll need:

- 1 [Powerboost 500](https://www.adafruit.com/products/1903)
- 1 [LiPoly battery](https://www.adafruit.com/products/328)

If you wanted to use it as a camera, you'll need:

- 1 [Raspberry Pi Camera](https://www.adafruit.com/products/3099)

It really depends. The circuit design for the phone can be found [here](https://learn.adafruit.com/piphone-a-raspberry-pi-based-cellphone/overview). While the camera 
can be found [here](https://www.raspberrypi.org/documentation/usage/camera). If you wanted to make something else, the 
hardware required would be different. What Cobblr provides is an easier way to make those devices, so you can focus on the 
hardware design.

# Opional CADs
I created a few devices using the Cobblr framwork. The CNC work I did with some of the devices isn't required to use Cobblr. However if you'd like to create those, I've put each in a my CAD repository.

- [Cobblr-Camera Hardware Design (CADs)](https://github.com/TheQYD/CAD/tree/master/cobblr-camera)
- [Cobblr-Phone Hardware Design (CADs)](https://github.com/TheQYD/CAD/tree/master/cobblr-phone)

These can be used to mill bodies for a phone or a camera. Using milling or 3d printing. I used Delrin, polycarbonate, and aluminum to make these devices using an Othermill(http://othermachine.co). However, they can also be 3D printed.

# How to Install Cobblr
1. Attach the PiTFT to the Raspberry Pi.
2. Follow the directions provided by Lady Ada to [install the kernel and configure it](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/overview)
3. When running the `adafruit-pitft-helper` during installation, select 'show console on screen'.
4. Perform the commands below.

```
git clone https://github.com/TheQYD/cobblr.git
cd cobblr
sudo ./preinstall.sh
sudo ./cobblr.py install cobblr
```

Next, you'll want to install apps.

# How to Install Applications
Once Cobblr is installed you can install apps for it. To install apps, from the command line, you simply enter:

`sudo cobblr install <app name>`

Currently, three apps run in landscape mode and three in portrait mode.

## Landscape
- cobblr-camera
- cobblr-video
- cobblr-audio

## Portrait
- cobblr-phone
- cobblr-calculator
- cobblr-music

I'm working on a way to have all apps work in both landscape and portrait mode.

# About Applications

Each app was meant to go with several devices I made. I've provided the CADs for those here, though Cobblr itself doesn't 
need them.

### cobblr-phone
A phone using the Adafruit Fona (SIM800).
![(Cobblr Images](photos/cobblr_phone.jpg?raw=true "Phone")

It's code can be found [Raspberry Zero] (https://github.com/TheQYD/cobblr-phone)

### cobblr-music
An MP3 player.
![(Cobblr Images](photos/cobblr_music.jpg?raw=true "Music")

It's code can be found [Raspberry Zero](https://github.com/TheQYD/cobblr-music)

### cobblr-calculator 
A calculator. It was created as a test to see how difficult it would be to create apps.
![(Cobblr Images](photos/cobblr_calculator.jpg?raw=true "Calculator")

It's code can be found [Raspberry Zero](https://github.com/TheQYD/cobblr-calculator)

### cobblr-camera
A camera. It has all of the effects and filters from picamera.
![(Cobblr Images](photos/cobblr_camera.jpg?raw=true "Camera")

It's code can be found [Raspberry Zero](https://github.com/TheQYD/cobblr-camera)

### cobblr-video
A video recorder. It records video (and audio if a mic is present).
![(Cobblr Images](photos/cobblr_video.jpg?raw=true "Video")

It's code can be found [Raspberry Zero](https://github.com/TheQYD/cobblr-video)

### cobblr-audio
Records audio and generates a spectrogram.
![(Cobblr Images](photos/cobblr_audio.jpg?raw=true "Audio")

It's code can be found [Raspberry Zero](https://github.com/TheQYD/cobblr-audio)

# The API
You don't have to use the Cobblr API to use Cobblr. I will write some API documentation for it when I get the time. However, I 
think it's easy enough to tinker with and get something if I discuss it a little.

The API is simple. Cobblr is just a state manager. All it does is give you an interface between your module and the 
touchscreen. In order to speak to the touchscreen, you'll have to use some functions it knows about. That's the API.

Cobblr keeps it's state in a module called SystemState. SystemState keeps track of lot's of stuff, but the most important to
you is the application_state and screen_mode. Each application is a high level state for cobblr, and each mode is a substate 
for the application. When Cobblr starts, it's in a state called desktop and it's mode is 1 -- ('desktop', 1). When you go to 
power down the system, for example, it's kept in ('desktop', 2). Each application_state is a new application, while each 
screen mode is the layout for that application.

So, to write a module you'll need:

1. A config file.
2. A module.
3. 40x40 pngs of the icons for each

The config file is kept in <application_name>/configs/<application_name>.config. The calculator, for example, is kept in
calculator/config/calculator.yaml. The buttons are kept in <application_name>/icons/<icon_name>.png. The basic parts of a
config file are:

```
application: <application_name>
icon-size: [40, 40]
Process: <bool>
Main: <bool>
Init: <bool>
Thread:<bool>
screen-modes:
  <screen_mode1>:
    <icon_name_a>: [x_position, y_position]
    <icon_name_b>: [x_position, y_position]
  <screen_mode2>:
    <icon_name_c>: [x_position, y_position]
    <icon_name_d>: [x_position, y_position]
```

Using the calculator example, here's what goes into the config file:

```
application: calculator
Init: True
Process: True
Thread: False
Main: False
icon-size: [40, 40]
screen-modes:
  1:
    # Row 1
    1: [1.5, 3]
    2: [2.75, 3]
    3: [4, 3]
   
    # Row 2
    4: [1.5, 4]
    5: [2.75, 4]
    6: [4, 4]
    
    # Row 3
    7: [1.5, 5]
    8: [2.75, 5]
    9: [4, 5]
    
    # Row 4
    point: [1.5, 6]
    0: [2.75, 6]
    alt: [4, 6]
 
    # Row 5
    right_parentheses: [1.5, 7]
    left_parentheses: [2.75, 7]
    delete: [4, 7]   
    
    # Column of Operators
    plus: [5.5, 3]
    minus: [5.5, 4]
    multiply: [5.5, 5]
    divide: [5.5, 6]
    equals: [5.5, 7]
    
    go_back: [5.88, 1.12]
```

Basically, the screen size is divided by 40. So, if you have a screen that's 320x240 it then becomes a 8x6 grid. Each number
for x and y is just a place in that grid where the icon goes. An icon name is simply the name of the icon minus .png. So, if
you want a button in the upper left hand corner of the screen, it would be at location 1,1. So, in the config file, you'd
simply add the name of the button, without the extension and it's location in the grid. For example, a go button that uses a
file called go.png would say:

``
go: [1, 1]
``

The application module goes in <application_name>/<application_name>.py. An __init__.py file is placed in this directory so
cobblr can initialize the module during startup. Each module must contain a Process() function. This function contains the
code that will be executed when the module is run. Other functions can be written in this module, or other modules can be
placed in the directory. The functions that go in a module have to be placed in the config file. Here's a discription of the
modules:

```
    Init():
      Init sets up the environement or starts services necessary for the module
      to run. It should contain a SystemState.<application_name> = <data> for any
      data that the module needs to track between instances (times you run the module).
    Process():
      Process runs when a button on the screen is pressed. It responds to the
      button press with an Screen. All functions that do anything when the screen
      is pressed should be placed here.
    Main():
      Main runs after switching to an application. Any computation or animation
      being done belongs in the Main function. Main can hold a while loop, but
      the conditioning would have to be rigged like this:
         " while SystemState.application == (application_name): "
    Thread():
      Similar to Main, but get's called when Cobblr is initialized. Thread is
      a part of the module that get's spawned as a thread from within
      init. If there is a set of tasks that the module must run outside of Cobblr's
      main thread.
```

If any of these four are used in your module, you must set it to 'True' in your config file. The desktop icon is then placed 
in the 'desktop' folder, then the desktop.yaml file in the desktop's `config/` is edited to reflect the position of this icon 
on the desktop. Installing the apps I've already made require none of this. 

Some required imports are

```
from engine import SystemState
from engine import Menu
from engine import TextWriter
```

Those three do very important things each module may need. For example, the module may need to store data against instances
of it being called. So, SystemState.<module_name> is necessary. You may also need data from Cobblr itself. It's kept there.
Menu contains the very importan Menu.Back() method. If you need to go back to the desktop, you'd make a go_back icon 
(you can use mine), and write a function that says:

```
if SystemState.pressed_button == 'go_back':
  Menu.Back()
```

That drops you back to whatever application (application_state) and menu (menu_state) you were in last. TextWriter is used to
write text on the screen. The code is pretty self explanitory. You just fill the function with data and use the screen's
location to write text. There are some more complicated bits in there, but I'll document that when I write the API docs.

I'm working on making it universal to anyone's apps anywhere. However, this is all you need to know to hack a quick app. If 
you want to contribute, go for it! I could use the help.

# Notes

This project started about 2 years ago when I tried Dave Hunt's PiPhone. I was so excited, I tried to add the ability to
recieve calls. That didn't work out, so I decided to slowly take it apart and try to understand what it was doing. I
eventually did, and decided to add the ability for others to contribute. And, here it is. I still have to document the API. 
Functionality wise, it's stable. But there are some things I may have to change about the API to support apps switching 
between landscape and portrait mode.

# License
Picolator is available under the MIT license. See the LICENSE file for more info. Make it better!
