# Jarduino - Arduino Sketches in a Jupyter Notebook Cell

*Designed for the Iron Python Kernel*

Many developers use Arduino boards to generate data to bring into a Jupyter Notebook, but need to compile/load/run their Arduino code from the Arduino IDE.

This code provides Jupyter Notebook magics to allow Arduino C (sketch) code in a Python cell to be compiled and loaded to the Arduino board by making use of the [command line features of the arduino command](https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc).

The code supports:

*  Multiple Arduino boards simultaneously connected to the computer
*  Separate Arduino board types (uno, nano, micro, etc.)

The magic supports the Arduino IDE's directory/file structure for saving sketch files (.ino), where, by default:
 *  By default, a sketch is saved in its own subdirectory with the same name as the file
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

> %jardutil?



## Magics provided

### %%jarduino <filename> 
*  Saves the contents of the cell to a .ino arduino file, compiles and loads it.
*  Optionally (--verify) compiles only without  loading
*  Respects the Arduino IDE convention of creating a subdirectory of the same name 
  *  Places that subdirectory within the *sketches* subdirectory to keep things tidy
  *  Allows you to override that by specifying another subdirectory under *sketches*. Read the tutorial to understand why this is important.
  
Parameters:
*  positional arguments: filename              file to write

Optional arguments:
*  --check, -c           Check/compile only. Do not load to Arduino board
*  --verbose, -v         Enable verbose mode during build/load
*  --dir DIR, -d DIR     The directory within sketches to store the file
*  --port PORT, -p PORT  The serial port connected to the Arduino
*  --board BOARD, -b B BOARD  Arduino board type

Usage example: the following in a Python cell

``` %%jarduino mysketch
void setup(){
    Serial.begin(9600);
    int x=10;
}
void loop(){
   x=x+1;
   Serial.println(x)
}
```
*  If not there, creates directory *sketches/* in the current directory
*  If not there, creates directory *sketches/mysketch* in the current directory
*  Saves everything after the first line into file sketches/mysketch/mysketch.ino. Overwrites the file if it already exists.
*  If file 

  

### %jardutil
Provides utility functions to identify connected Arduino boards and ports.

Parameters:
*  -- ports-p: list ports and connected Arduino board types
*   --dirlist DIRECTORY, -d  DIRECTORY: ;list all arduino sketch files in specified directory under sketches directory

  

