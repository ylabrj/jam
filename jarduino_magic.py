"""Implementation Jupyter IPython magic functions for
Arduino compile/execute load.
"""
# Copyright (c) Rene Juneau
# Distributed under the terms of the Modified BSD License.

# These imports required for the functions we run in our magic
import io
import os
import subprocess
import serial
import serial.tools.list_ports

# These imports required for the magic function decorators that process
# command line parameters for us
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class


#######
# Utility functions

# Return list of Arduino ports
def get_arduino_ports():
    return([p.device for p in serial.tools.list_ports.comports()
                            if 'Arduino' in p.description])




# Create our overall class - JarduinoMagics
# The class could contain multiple magics.
 
@magics_class
class JarduinoMagics(Magics):
    """Magics to save, compile and load Arduino code from a Python cell
    """
    ###############################
    # Magic: jarduino
    #
    # This magic saves, compiles and optionally loads the Arduino found in the cell after the
    # %%jarduino <filename>
    
    # It's a cell magic (@cell_magic) because it's going access the full
    # contents of the cell - the Arduino code we want to compile  and load
    # The @ things are function decorators to manage the command line parameters
    
    @cell_magic
    
    # This sets us up to use the built-in Jupyter magics arguments toolkit
    @magic_arguments.magic_arguments()
    # We have an @magics_argument.argument line for each parameter.
    # We can have as many as we want.
    # The first arguments are flags - enabled or not.
    # 

    @magic_arguments.argument('--check', '-c', action='store_true',
        help='Check/compile only. Do not load to Arduino board')
    @magic_arguments.argument('--verbose', '-v', action='store_true',
        help='Enable verbose mode during build/load')
    #The next ones provide a parameter value
    #   The directory name
    @magic_arguments.argument('--dir', '-d', 
        help='The directory within sketches to store the file')
        #   The port
    @magic_arguments.argument('--port', '-p', 
        help='The serial port connected to the Arduino')
        #   The directory name
    @magic_arguments.argument('--board', '-b', 
        help='Arduino board type')
    # Finally, the file name, which has no - or -- identifier.
    @magic_arguments.argument( 'filename', type=str,
        help='file to write')
    # Now we finally get on to our function
    def jarduino(self, line, cell):
        """Compiles, loads and runs the cell contents to the speccified board.Write the contents of the cell (an Arduino sketch) to the specified name and directory within
        the sketches subdirectory of the notebook.

        But first saves the cell contents to the specified directory. Default directory
        is sketches/<filename>.

	Example: jarduino mysketch
        - If not there, creates directory sketches
        - If not there, creates directory sketches/mysketch
        - Places the content of the cell in file sketches/mysketch/mysketch.ino
        """
        args = magic_arguments.parse_argstring(self.jarduino, line)
        # filename is all alone on the command line with no -x or --identifier
        # that's parsed out by default by the magic arguments parser because
        # we specified it above.
        filename=args.filename

        # By default, the Arduino IDE puts each sketch its own directory
        # with the same name as the file. So that's our default as well. 
        # Multiple sketches can be in the same directory, but they can't
        # share function names. That creates an error if we have two
        # independent sketches with their own void() and/or setup() functions.
        # Because multiple sketches in the same directory
        # get compiled as one big file. That's the Arduino IDE way.
        
        # Just so our notebook isn't cluttered, we put all the sketch
        # directories under a subdirectory called "sketches"
        if not(os.path.isdir("sketches")):
            print("Creating sketches directory for first time in notebook")
            os.mkdir("sketches")
                              
        # If no directory specified with -d or --dir on the command line,
        # use the filename as directory name. Same default as Arduino IDE                    
        if args.dir is None:
            filedir = filename
        # otherwise, use the one specified.                      
        else:
            filedir = args.dir
        # If the directory isn't there, create it.
        if not(os.path.isdir("sketches/"+filedir)):    
            print("Creating sketch directory sketches/"+filedir)
            os.mkdir("sketches/"+filedir)
            

        # Get the Arduino ports available

                              
        # Build the full path and write it out the file
        #filename = os.getcwd()+"/sketches/"+filedir+"/"+filename+".ino"
        filename = "sketches\\"+filedir+"\\"+filename+".ino"
        if os.path.exists(filename):
            print("Overwriting %s" % filename)
        else:
            print("Writing %s" % filename)
        mode = 'w' 
        with io.open(filename, mode, encoding='utf-8') as f:
            f.write(cell)

        # Start the string for the Arduino command line options
        # Load to board or just compile and validate?
        if args.check:
            build_option = '--verify'
            print("-- check option: Compile only - will not attempt to load to board")                 
        else:
            build_option = '--upload'   # Full validate/compile/upload
            print("Build will upload to board if compile successful")

        # Figure out which port to use


        arduino_ports = [p.device for p in serial.tools.list_ports.comports()
                            if 'Arduino' in p.description]
        # If there are no Arduino ports found, only run if --check option enable 
        if not(arduino_ports): 
            if not(args.check):
                print('No Arduino ports found. Run with -c to check and not upload')
                exit()
        # Now figure out which port to use, or, if specified, 
        else:
                      
            if (args.port):
                if args.port in arduino_ports:
                    arduino_port = args.port
                else:
                    print('Port', args.port, 'not found. Available ports:', arduino_ports)
                    exit()
            else:
                arduino_port = arduino_ports[0]
                if len(arduino_ports) > 1:
                      print('Warning: Multiple Arduino ports found:', arduino_ports)
            print('Using arduino port', arduino_port)
            build_option +=' --port ' + arduino_port

      
        if args.verbose:
            build_option += ' --verbose'

        if args.board:
            build_option += ' --board arduino:avr:' + args.board    





        print("Starting Arduino build")
        pcmd = '"C:\\Program Files (x86)\\Arduino\\arduino.exe" '+ build_option + ' ' +filename
        print('Command: ', pcmd)
        p = subprocess.Popen(pcmd, stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE, shell=True)
        #p = subprocess.Popen(["C:/Program Files (x86)/Arduino/arduino.exe "+build_option
        #          build_option, port_option, filename], stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE, shell=True)
 

        (output, err) = p.communicate()
 
        # Wait for command to terminate. And dump the output
        p_status = p.wait()
        print("Command output : ", output.decode('utf-8'))
        print("Command errors: ", err.decode('utf-8'))
        # Commented this out because it always gives 0 anyway.
        # print("Command exit status/return code : ", p_status)
        print("Done")
              

    # end jarduino ########################################


    ###############################
    # Magic: jardutil
    #
    # Runs utilities against the Arduino ports and code.
    #
    # It's a line magic (@line_magic) because it only cares about the parameters on the line
    # and not the rest of the cell.
    #
    # See comments for the arduino magic above for how all these weird @ things work for
    # defining parameters
    
    @line_magic
    
    # This sets us up to use the built-in Jupyter magics arguments toolkit
    @magic_arguments.magic_arguments()
    # We have an @magics_argument.argument line for each parameter.
    # We can have as many as we want.
    # The first arguments are flags - enabled or not.
    # 

    @magic_arguments.argument('--ports', '-p', action='store_true',
        help='List available Arduino-connected ports')
    # Commented out --getprefs and --version because Windows arduino command doesn't support
    #@magic_arguments.argument('--getprefs', '-g', action='store_true',
    #    help='Show current default preferences/settings of the Arduino IDE')
    #@magic_arguments.argument('--version', '-v', action='store_true',
    #    help='Show version of the installed Arduino IDE')
    #The next ones provide a parameter value
    #   List all arduino sketches from the directory
    @magic_arguments.argument('--dirlist', '-d', 
        help='List all arduino sketch files in specified directory under sketches directory')

    # Now we finally get on to our function
    def jardutil(self, line):
        '''jardutil: utility for reading arduino configuration from system
        '''
        args = magic_arguments.parse_argstring(self.jardutil, line)

        build_option = ''
        
        if args.ports:
            print('Arduino ports on system:')
            print([p.description for p in serial.tools.list_ports.comports()
                   if 'Arduino' in p.description])
## Commented out because the options don't work on windows            
##        if args.getprefs:
##            print('Current Arduino IDE preference settings:')
##            build_option += ' --get-pref'
##        if args.version:
##            build_option += ' --version'

        if args.dirlist:
            adir = 'sketches/'+args.dirlist
            print('Files in', adir,':')
            print(os.listdir(adir))

        if build_option != '':
            p = subprocess.Popen(["C:/Program Files (x86)/Arduino/arduino.exe",
                 build_option], stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE, shell=True)

            (output, err) = p.communicate()
 
            # Wait for command to terminate. And dump the output
            p_status = p.wait()
            print("Command output : ", output.decode('utf-8'))
            print("Command errors: ", err.decode('utf-8'))


        
    #end jardutil ######################################


            
            
            
    

# Register the magics in the Ipython kernel

ip = get_ipython()
ip.register_magics(JarduinoMagics)




