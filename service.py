#!/usr/bin/python
import mraa

import sys
import os
import atexit

FIFO = 'led.fifo'

# On exit, clean up
@atexit.register
def cleanup():
    try:
        os.unlink(FIFO);
    except:
        pass;

LED_R = None
LED_G = None
LED_B = None

# Setup the GPIOs for output
def setup_led():
    global LED_R, LED_G, LED_B

    LED_R = mraa.Gpio(20);
    LED_R.dir(mraa.DIR_OUT);
    LED_G = mraa.Gpio(19);
    LED_G.dir(mraa.DIR_OUT);
    LED_B = mraa.Gpio(18);
    LED_B.dir(mraa.DIR_OUT);

# Switch the GPIOs for the led
def switch_led(red, green, blue):
    global LED_R, LED_G, LED_B

    LED_R.write(red);
    LED_G.write(green);
    LED_B.write(blue);

def main():
    # Make the fifo, if it exists, remake it
    try:
        os.mkfifo(FIFO);
    except:
        cleanup();
        main();
        return;

    print("Daemon started!");
    # Keep going forever
    while True:
        # Open the fifo and read out all the lines
        with open(FIFO) as fifo:
            for line in fifo:
                # Check that lines are 4 characters long
                if(len(line) != 4):
                    print("Invalid input format!");
                    print("Expected:\t[0-1][0-1][0-1]");
                    print("Examples:\t000, 001, 010, ...");
                    print("Got:\t\t" + line);
                    print();
                    continue;

                # Check that line ends with newline
                # - Actually an invariant by readline()
                if(line[3] != '\n'):
                    print("Invalid input format!");
                    print("Expected:\tNewline in string pos 4");
                    print("Got:\t\t" + line[3]);
                    print();
                    continue;

                # Parse out R,G,B values
                red     = None;
                green   = None;
                blue    = None;
                try:
                    red     = int(line[0]);
                    green   = int(line[1]);
                    blue    = int(line[2]);
                except:
                    print("Invalid input format!");
                    print("Expected:\t[0-1][0-1][0-1]");
                    print("Examples:\t000, 001, 010, ...");
                    print("Got:\t\t" + line);
                    print();
                    continue;

                # Switch led state
                #print("Setting RGB Led!");
                #print("RED:\t" + str(red));
                #print("GREEN:\t" + str(green));
                #print("BLUE:\t" + str(blue));

                switch_led(red, green, blue);

# Setup hardware leds
setup_led();

# Turn on blue
switch_led(0,0,1);

# Run main loop
main();
