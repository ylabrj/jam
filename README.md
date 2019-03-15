# jam - Jupyter Notebook and Arduino Mash-Up using cell magics

### Formerly jarduino until I found out the java people already used that name

*Designed for the Iron Python Kernel*

## WARNINGS:
*  Tested on Windows 10 and Raspberry Pi 4.14
*  Still in development, but good enough that people have been asking me to share it.
*  For MAC and Linux, always specify the serial port with --port option
*  If things hang, just restart the kernel
*  __USE *--redefine* with caution.__ It does not back up a file first. There was one glitch I have not been able to reproduce that corrupted a file. I'll be adding a feature to keep the original and restore it.

## Overview

Many developers use Arduino boards to generate data to bring into a Jupyter Notebook, but need to compile/load/run their Arduino code from the Arduino IDE.

This code provides Jupyter Notebook magics to allow Arduino C (sketch) code in a Python cell to be compiled and loaded to the Arduino board by making use of the [command line features of the arduino command](https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc).

The code is designed to be as compatible as possible with the behaviour of the Arduino IDE and its serialplotter functions, while offering improved support for parameters at the cell and magic level for:

*  Multiple Arduino boards simultaneously connected to the computer
*  Separate Arduino board types (uno, nano, micro, etc.)

The magic supports the Arduino IDE's directory/file structure for saving sketch files (.ino), where, by default:

 *  A sketch is saved in its own subdirectory with the same name as the file
 *  Multiple sketches located in the same directory are automatically compiled as one file. In the Arduino IDE, the multiple files are presented as separate tabs in the IDE. 

To keep the notebook tidy, all the sketch directories are kept under directory *sketches*.

A design document with tutorial code and usage examples will be provided later.

## Tutorial on jam - and on running Arduino sketches without jam.

The [Integrating Arduino and Jupyter tutorial](https://nbviewer.jupyter.org/github/ylabrj/jam/blob/master/Integrating%20Arduino%20and%20Python%20in%20a%20Jupyter%20IPython%20Notebook%20with%20jam.ipynb) in this repository is a Jupyter notebook, so it cannot be viewed directly. The link makes it available through nbviewer.

The tutorial takes you through some usage scenarios and design decisions. Useful, because it shows you how to use some of the default magics to save and run Arduino code without jam. But hopefully you'll agree that it's better with jam.

## Installation

*  We recommend a full [Anaconda installation](https://www.anaconda.com/distribution/) (not just Jupyter Notebook) because the graphing functions make use of *matplotlib*, *numpy* and *pandas* Python libraries. These are all included with the Anaconda.
*  The Arduino IDE must be installed on your system. Go to the __*Download the Arduino IDE*__ section of [this page](https://www.arduino.cc/en/Main/Software)
*  __RASPBERRY PI: DO NOT USE THE RASPBERRY PI RASPBIAN'S ARDUINO PACKAGE DOWNLOAD.__ The Raspbian package manager is providing an ancient version of Arduino IDE that does not support command line execution. Instead, download the most recent version from [arduino.cc](https://www.arduino.cc/en/Main/Software).
*  __WINDOWS: Add the directory with the Arduino command (Arduino or Arduino.exe) to your command path.__
*  Download or copy file __*jam.py*__  to the user's Jupyter Notebook startup directory. Jupyter will load it at startup, or you can run a kernel restart within your notebook to load it. The startup directory is located under your home directory at

 > .ipython/profile_default/startup/
 
 The functions are available through two magics:
 
 *  __%%jamcellcell__ is a Python cell magic where the rest of the cell is the Arduino code (instead of Python code!)
 *  __%jam__ is a Python line magic that operates on existing sketch files and provides utility functions and graphing extensions.

Test and get current parameters by entering the following in a Python cell:

> %%jamcellcell?

> %jam?

## %%jamcell <filename> 
*  Saves the contents of the cell to a .ino arduino file, compiles and loads it.
*  Respects the Arduino IDE convention of creating a subdirectory of the same name 
  *  Places that subdirectory within the *sketches* subdirectory to keep things tidy
  *  Allows you to override that by specifying another subdirectory under *sketches*. Read the tutorial to understand why this is important.
  
Parameters:
*  positional arguments: filename              file to write. With or without the *.ino* extension

Optional arguments:
*  --check, -c           Check/compile only. Do not load to Arduino board
*  --verbose, -v         Enable verbose mode during build/load
*  --dir DIR, -d DIR     The directory within directory *sketches/* to store the file This overrides the filename.
*  --port PORT, -p PORT  The serial port to which the Arduino is connected
*  --board BOARD, -b B BOARD  Arduino board type
*  --redefine NAME VALUE  Changes the #define NAME value in the saved file while leaving the cell intact. __*Note*:__ *In a big stupid, I forgot that #define only applies to numbers, and not strings. --redefine will handle strings that even have spaces. But the sketch/C code only allows numbers in constants. We'll fix that later with --reconstant or something.

Usage example: the following in a Python cell

``` %%jamcell mysketch
#define INCREMENT 10
void setup(){
    Serial.begin(9600);
    int x = 1;
}
void loop(){
   x=x + INCREMENT;
   Serial.println(x)
}
```
*  If not there, creates directory *sketches/* in the current directory
*  If not there, creates directory *sketches/mysketch* in the current directory
*  Saves everything after the first line into file sketches/mysketch/mysketch.ino. Overwrites the file if it already exists.
*  Compiles and loads the code to the default Arduino board

With the same Arduino code in the cell:

> %%jamcell mysketch --dir yoursketch

*  Stores the file in directory *sketches/yoursketch/* instead of the default */sketches/mysketch*
*  You can use a fully-qualified path to override the *sketches/* directory

> %%jamcell mysketch --board micro --port COM5

* Communicates with the Arduino board on COM5
* Identifies to the IDLE that the board is an Arduino Micro

> %%jamcell mysketch --redefine INCREMENT 20
*  Saves the file but first replaces *#define INCREMENT 10* with *#define INCREMENT 20


## %jam
Provides utility functions to identify connected Arduino boards and ports and provide plotting assistance. Plotting configuration is defined later in this README.

__Parameters - simple utility__
*  -- ports-p: list ports and connected Arduino board types
*  --dirlist DIRECTORY, -d  DIRECTORY: list all arduino sketch files in specified directory under sketches directory
*  --plot XX: plot the next XX points on the serial line in to a static matplotlib directory. Requires *%matplotlib inline* before *%jam* in the cell. 
*  --plotext <program>: start <program> as a serial plotter. The Arduino IDE would be an example if you want to use its serialplotter function.

__Parameters - operations on existing sketch files__
*  --sketch <sketchname>: the sketch to load and compile. Works with --dir if it's not located in the expected default directory *sketches/<sketchname>
*  --redefine works the same way as it does for %%jamcell, with the advantage that you can have multiple %jams in the same cell. In the following example, we can send the same I2C client program to three different connected Arduino boards but assign each one with a different I2C bus address:
 
 '''
 %jam --sketch i2csketch --port COM5 --board uno --redefine I2C_ADDR 04
 %jam --sketch i2csketch --port COM6 --board micro --redefine I2C_ADDR 06
 %jam --sketch i2csketch --port COM8 --board mega --redefine I2C_ADDR 08
 '''
 
## Plotting considerations

### Compatibility with Arduino IDE serialplotter

The serial plotter on the Arduino IDE expects numbers in character string separated by tabs or spaces. If there are multiple numbers on the line, it will make multiple plots.

### Static plotting with --plot
The *--plot XX* option behaves the same way as the Arduino IDE but is not a dynamic plot. It accumulates XX data points (from Serial.println() in the Arduino sketch) and then plots them all all at once.

The plots overlap. Adding the *--stack* option separate the plots by stacking the graphs.

### External live plotting

We're still working on having live plots inside the notebook.

In the interim, you can specify an external plotter by adding *--plotext <program>*. The external plotter must support the same ASCII number format from the *Serial.println()* output. <program> must be configured in the system path or entered with a fully-qualified path.
 
The Arduino IDE serialplotter cannot be called up directly from the command line. You can enter *--plotext Arduino* but then you'll need to execute the pulldown menu option and specify the serial port to start it. __*Caution: Starting the Arduino IDE serial plotter resets the Arduino board.*__

__[serialplot](https://hackaday.io/project/5334-serialplot-realtime-plotting-software)__ is a free option we like that has great performance. You may need to specify the port, and then hit the start button to start plotting.


## Known issues

So far only tested on Windows 10 and Raspberry Pi Raspbian 4.14
Thanks to Calin Graza for starting the MAC testing.

__--redefine__ works on numbers and strings - but the C/sketch compiler only supports numbers. Duh.

If the underlying program (plotter, Arduino IDE) errors out or there is contention on the serial port, the IPython kernel can be locked up. Restarting the kernel fixes it nicely.

Still working on getting live plotting working.


### MAC Darwin, Linux and Raspberry Pi serial port issues.
The Windows operating system information calls identify ports as connected to Arduino devices directly in the Python serial library calls. The magics use this to identifythe Arduino ports and/or verify that a selected port is an Arduino port.

Mac/Darwin and Linux do not provide this info to the Python serial library , so port checks are not performed. Serial port listing functions simply list all the available serial ports. The documentation says the IDE will recall the last port used, but we have found this unreliable. Always specify the --port. Also good practice to specify the board type with --board.


