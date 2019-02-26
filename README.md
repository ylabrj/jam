# Jarduino - Arduino Sketches in a Jupyter Notebook Cell

*Designed for the Iron Python Kernel*

Many developers use Arduino boards to generate data to bring into a Jupyter Notebook, but need to compile/load/run their Arduino code from the Arduino IDE.

This code provides Jupyter Notebook magics to allow Arduino C (sketch) code in a Python cell to be compiled and loaded to the Arduino board by making use of the [command line features of the arduino command](https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc).

The code supports:

*  Multiple Arduino boards simultaneously connected to the computer
*  Separate Arduino board types (uno, nano, micro, etc.)
*  The Arduino IDE's sketch file (.ino) organisation where, by default, 
 *  The sketch is saved in its own subdirectory with the same name as the file
 *  Multiple sketches located in the same directory are automatically compiled as one file. In the Arduino IDE, the multiple files are presented as separate tabs in the IDE.
 
To keep the notebook tidy, all the sketch directories are kept in directory *sketches*

A design document with tutorial code and usage examples is provided XXX here XXX

## Installation

Download or copy file __*arduino_magics.py*__ needs to the user's Jupyter Notebook startup directory. Jupyter will load it at startup, or you can run a kernel restart within your notebook to load it. The startup directory is located at:
*  __Windows:__ c:\users\<username\.ipython\profile_default\startup\
*  __Raspberry Pi:__
*  __MAC:__

Test and get currentby entering the following in a Python cell:

> %%jarduino?



## Magics provided

### %%jarduino <filename> 
*  Saves the contents of the cell to a .ino arduino file, compiles and loads it.
*  Optionally (--verify) compiles only without  loading
*  Respects the Arduino IDE convention of creating a subdirectory of the same name 
  *  Places that subdirectory within the *sketches* subdirectory to keep things tidy
  *  Allows you to override that by specifying another subdirectory under *sketches*. Read the tutorial to understand why this is important.
  
Parameters:

  

### %jardutil
*  Provides utility functions to identify connected Arduino boards and ports.
*  -p: list ports and port types

  

