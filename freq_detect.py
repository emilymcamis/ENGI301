"""
--------------------------------------------------------------------------
Frequency Detector
--------------------------------------------------------------------------
License:   
Copyright 2020 Emily McAmis

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Describe here
"""
# Import required programs
"""import Adafruit_BBIO.EDC as ADC"""
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import ht16k33 as HT16K33
import time
import sound_analysis
#import sound_analysis as SA

#Import sound analysis tools
"""from scipy import arange
import numpy, sci
import pylab
import matplotlib
import pyaudio
import struct"""

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Functions / Classes

class FrequencyDetector():
    """ FrequencyDetector """
    blue_led_A         = None
    blue_led_A_on      = None
    blue_led_B         = None
    blue_led_B_on      = None
    blue_led_C         = None
    blue_led_C_on      = None
    blue_led_D         = None
    blue_led_D_on      = None
    blue_led_E         = None
    blue_led_E_on      = None
    blue_led_F         = None
    blue_led_F_on      = None
    blue_led_G         = None
    blue_led_G_on      = None
    green_led          = None
    green_led_on       = None
    yellow_led_sharper = None
    yellow_led_sharper_on = None
    yellow_led_sharp   = None
    yellow_led_sharp_on = None
    yellow_led_flat    = None
    yellow_led_flat_on = None
    yellow_led_flatter = None
    yellow_led_flatter_on = None
    display            = None


    def __init__(self,  blue_led_A="P2_2", blue_led_B="P2_4", blue_led_C="P2_6",
                       blue_led_D="P2_8", blue_led_E="P2_10", blue_led_F="P2_18",
                       blue_led_G="P2_20", yellow_led_flatter="P2_22", 
                       yellow_led_flat="P2_24", green_led="P2_33", 
                       yellow_led_sharp="P2_35", yellow_led_sharper="P1_34",  
                       i2c_bus=1, i2c_address=0x70):
        """ Initialize variables and set up display """
        self.green_led             = green_led
        self.blue_led_A            = blue_led_A
        self.blue_led_B            = blue_led_B
        self.blue_led_C            = blue_led_C
        self.blue_led_D            = blue_led_D
        self.blue_led_E            = blue_led_E
        self.blue_led_F            = blue_led_F
        self.blue_led_G            = blue_led_G
        self.yellow_led_sharper    = yellow_led_sharper
        self.yellow_led_sharp      = yellow_led_sharp
        self.yellow_led_flat       = yellow_led_flat
        self.yellow_led_flatter    = yellow_led_flatter
        self.display               = HT16K33.HT16K33(i2c_bus, i2c_address)
        self.blue_led_A_on         = False
        self.blue_led_B_on         = False
        self.blue_led_C_on         = False
        self.blue_led_D_on         = False
        self.blue_led_E_on         = False
        self.blue_led_F_on         = False
        self.blue_led_G_on         = False
        self.green_led_on          = False
        self.yellow_led_sharper_on = False
        self.yellow_led_sharp_on   = False
        self.yellow_led_flat_on    = False
        self.yellow_led_flatter_on = False
        
        self._setup()

    def _setup(self):
        """Setup the hardware components."""
    
        # Initialize Display
        self.set_display_dash()

        """# Initialize Button
        GPIO.setup(self.button, GPIO.IN)"""
        
        # Initialize LEDs
        GPIO.setup(self.yellow_led_sharper, GPIO.OUT)
        GPIO.setup(self.yellow_led_sharp, GPIO.OUT)
        GPIO.setup(self.yellow_led_flat, GPIO.OUT)
        GPIO.setup(self.yellow_led_flatter, GPIO.OUT)
        
        GPIO.setup(self.green_led, GPIO.OUT)

        GPIO.setup(self.blue_led_A, GPIO.OUT)
        GPIO.setup(self.blue_led_B, GPIO.OUT)
        GPIO.setup(self.blue_led_C, GPIO.OUT)
        GPIO.setup(self.blue_led_D, GPIO.OUT)
        GPIO.setup(self.blue_led_E, GPIO.OUT)
        GPIO.setup(self.blue_led_F, GPIO.OUT)
        GPIO.setup(self.blue_led_G, GPIO.OUT)
    # End def


# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------
    
    def set_display_dash(self):
        """Set display to word "----" """
        self.display.text("----")
    
    #Flag LEDs based on frequency value
    def determine_LEDs(self, frequency):
        
        #Set all initial flags to false so that LEDs clear between readings
        self.blue_led_A_on = False
        self.blue_led_B_on = False
        self.blue_led_C_on = False
        self.blue_led_D_on = False
        self.blue_led_E_on = False
        self.blue_led_F_on = False
        self.blue_led_G_on = False
       
        self.green_led_on = False
        
        self.yellow_led_flatter_on = False
        self.yellow_led_flat_on = False
        self.yellow_led_sharp_on = False
        self.yellow_led_sharper_on = False
        
        #The following if statements check which LEDs are flagged based on the 
        #frequency
        
        #A - in-tune
        if frequency in [110, 220, 440, 880, 1760, 3520]:
            self.blue_led_A_on = True
            self.green_led_on = True

        #A flatter
        a_flatter = []
        for num in range (208,214):
            a_flatter.append(num)
        for num in range (415, 428):
            a_flatter.append(num)
        for num in range (831, 856):
            a_flatter.append(num)
        for num in range (1712, 1759):
            a_flatter.append(num)    
        for num in range (3322, 3421):
            a_flatter.append(num)
    
        if frequency in a_flatter:
            self.blue_led_A_on = True
            self.yellow_led_flatter_on = True
    
        #A flat
        a_flat = []
        for num in range (106, 108):
            a_flat.append(num)
        for num in range (214,220):
            a_flat.append(num)
        for num in range (431, 439):
            a_flat.append(num)
        for num in range (851, 879):
            a_flat.append(num)
        for num in range (1801, 1864):
            a_flat.append(num)
        
        if frequency in a_flat:
            self.blue_led_A_on = True
            self.yellow_led_flat_on = True
        
        #A sharp
        a_sharp = []
        for num in range (221, 227):
            a_sharp.append(num)
        for num in range (441,452):
            a_sharp.append(num)
        for num in range (881, 905):
            a_sharp.append(num)
        for num in range (1761, 1811):
            a_sharp.append(num)
        
        if frequency in a_sharp:
            self.blue_led_A_on = True
            self.yellow_led_sharp_on = True
        
        #A sharper
        a_sharper = []
        for num in range (228, 233):
            a_sharper.append(num)
        for num in range (453,466):
            a_sharper.append(num)
        for num in range (906, 932):
            a_sharper.append(num)
        for num in range (1812, 1864):
            a_sharper.append(num)

        if frequency in a_sharper:
            self.blue_led_A_on = True
            self.yellow_led_sharper_on = True
        
        #B - in-tune
        if frequency in [247, 494, 988, 1976]:
            self.blue_led_B_on = True
            self.green_led_on = True
        
        #B flat
        b_flat = []
        for num in range (241, 246):
            b_flat.append(num)
        for num in range (481,493):
            b_flat.append(num)
        for num in range (951, 987):
            b_flat.append(num)
        for num in range (1920, 1975):
            b_flat.append(num)
        
        if frequency in b_flat:
            self.blue_led_B_on = True
            self.yellow_led_flat_on = True
        
        #B flatter
        b_flatter = []
        for num in range (234, 240):
            b_flatter.append(num)
        for num in range (467,480):
            b_flatter.append(num)
        for num in range (933, 950):
            b_flatter.append(num)
        for num in range (1865, 1919):
            b_flatter.append(num)
        
        if frequency in b_flatter:
            self.blue_led_B_on = True
            self.yellow_led_flatter_on = True
            
        #C - in-tune
        if frequency in [262, 523, 1047]:
            self.blue_led_C_on = True
            self.green_led_on = True
        
        #C sharp
        c_sharp = []
        for num in range (263, 270):
            c_sharp.append(num)
        for num in range (524, 539):
            c_sharp.append(num)
        for num in range (1048, 1078):
            c_sharp.append(num)
        for num in range (2094, 2194):
            c_sharp.append(num)
        
        if frequency in c_sharp:
            self.blue_led_C_on = True
            self.yellow_led_sharp_on = True

        #C sharper
        c_sharper = []
        for num in range (271, 277):
            c_sharper.append(num)
        for num in range (540, 554):
            c_sharper.append(num)
        for num in range (1079, 1109):
            c_sharper.append(num)
        for num in range (2195, 2217):
            c_sharper.append(num)
        
        if frequency in c_sharper:
            self.blue_led_C_on = True
            self.yellow_led_sharper_on = True
    
        #D - in-tune
        if frequency in [294, 587, 988, 1175]:
            self.blue_led_D_on = True
            self.green_led_on = True
        
        #D flat
        d_flat = []
        for num in range (286, 293):
            d_flat.append(num)
        for num in range (571, 586):
            d_flat.append(num)
        for num in range (1143, 1174):
            d_flat.append(num)
        for num in range (2289, 2348):
            d_flat.append(num)
        
        if frequency in d_flat:
            self.blue_led_D_on = True
            self.yellow_led_flat_on = True
        
        #D flatter
        d_flatter = []
        for num in range (278, 285):
            d_flatter.append(num)
        for num in range (555, 570):
            d_flatter.append(num)
        for num in range (1110, 1142):
            d_flatter.append(num)
        for num in range (2218, 2288):
            d_flatter.append(num)
        
        if frequency in d_flatter:
            self.blue_led_D_on = True
            self.yellow_led_flatter_on = True
       
        #D sharp
        d_sharp = []
        for num in range (295, 303):
            d_sharp.append(num)
        for num in range (588, 608):
            d_sharp.append(num)
        for num in range (1175, 1205):
            d_sharp.append(num)
        for num in range (2349, 2419):
            d_sharp.append(num)
        
        if frequency in d_sharp:
            self.blue_led_D_on = True
            self.yellow_led_sharp_on = True

        #D sharper
        d_sharper = []
        for num in range (304, 320):
            d_sharper.append(num)
        for num in range (609, 622):
            d_sharper.append(num)
        for num in range (1206, 1245):
            d_sharper.append(num)
        for num in range (2420, 2489):
            d_sharper.append(num)
        
        if frequency in d_sharper:
            self.blue_led_D_on = True
            self.yellow_led_sharper_on = True
    
        #E - in-tune
        if frequency in [330, 659, 988, 1319]:
            self.blue_led_E_on = True
            self.green_led_on = True

        #E flatter
        e_flatter = []
        for num in range (312, 320):
            e_flatter.append(num)
        for num in range (623, 637):
            e_flatter.append(num)
        for num in range (1246, 1280):
            e_flatter.append(num)
        for num in range (2490, 2564):
            e_flatter.append(num)
        
        if frequency in e_flatter:
            self.blue_led_E_on = True
            self.yellow_led_flatter_on = True

        #E flat
        e_flat = []
        for num in range (321, 329):
            e_flat.append(num)
        for num in range (638, 658):
            e_flat.append(num)
        for num in range (1281, 1318):
            e_flat.append(num)
        for num in range (2565, 2637):
            e_flat.append(num)
        
        if frequency in e_flat:
            self.blue_led_E_on = True
            self.yellow_led_flat_on = True  
    
        #F4 to F6 
        if frequency in [349, 494, 988, 1976]:
            self.blue_led_F_on = True
            self.green_led_on = True
    
        #G in-tune
        if frequency in [196, 698, 1397]:
            self.blue_led_G_on = True
            self.green_led_on = True
        
        #G sharp
        g_sharp = []
        for num in range (197,202):
            g_sharp.append(num)
        for num in range (393, 401):
            g_sharp.append(num)
        for num in range (785, 805):
            g_sharp.append(num)
        for num in range (1569, 1609):
            g_sharp.append(num)    
        for num in range (3137, 3229):
            g_sharp.append(num)
    
        if frequency in g_sharp:
            self.blue_led_G_on = True
            self.yellow_led_sharp_on = True

        #G sharper
        g_sharper = []
        for num in range (202,207):
            g_sharper.append(num)
        for num in range (402, 414):
            g_sharper.append(num)
        for num in range (806, 830):
            g_sharper.append(num)
        for num in range (1610, 1660):
            g_sharper.append(num)    
        for num in range (3230, 3321):
            g_sharper.append(num)
    
        if frequency in a_flatter:
            self.blue_led_A_on = True
            self.yellow_led_flatter_on = True

    #Update all LEDs
    def update_LEDs(self):
        if self.blue_led_A_on:
            GPIO.output(self.blue_led_A, GPIO.HIGH)
        else:
            GPIO.output(self.blue_led_A, GPIO.LOW)
            
        if self.blue_led_B_on:
            GPIO.output(self.blue_led_B, GPIO.HIGH)
        else:
            GPIO.output(self.blue_led_B, GPIO.LOW)
        
        if self.blue_led_C_on:
            GPIO.output(self.blue_led_C, GPIO.HIGH)
        else:
            GPIO.output(self.blue_led_C, GPIO.LOW)
        
        if self.blue_led_D_on:
            GPIO.output(self.blue_led_D, GPIO.HIGH)
        else:
            GPIO.output(self.blue_led_D, GPIO.LOW)
        
        if self.blue_led_E_on:
            GPIO.output(self.blue_led_E, GPIO.HIGH)
        else:
            GPIO.output(self.blue_led_E, GPIO.LOW)
        
        if self.blue_led_F_on:
            GPIO.output(self.blue_led_F, GPIO.HIGH)
        else:
            GPIO.output(self.blue_led_F, GPIO.LOW)
        
        if self.blue_led_G_on:
            GPIO.output(self.blue_led_G, GPIO.HIGH)
        else:
            GPIO.output(self.blue_led_G, GPIO.LOW)
        
        if self.green_led_on:
            GPIO.output(self.green_led, GPIO.HIGH)
        else:
            GPIO.output(self.green_led, GPIO.LOW)
        
        if self.yellow_led_flat_on:
            GPIO.output(self.yellow_led_flat, GPIO.HIGH)
        else:
            GPIO.output(self.yellow_led_flat, GPIO.LOW)
        
        if self.yellow_led_flatter_on:
            GPIO.output(self.yellow_led_flatter, GPIO.HIGH)
        else:
            GPIO.output(self.yellow_led_flatter, GPIO.LOW)
        
        if self.yellow_led_sharp_on:
            GPIO.output(self.yellow_led_sharp, GPIO.HIGH)
        else:
            GPIO.output(self.yellow_led_sharp, GPIO.LOW)
        
        if self.yellow_led_sharper_on:
            GPIO.output(self.yellow_led_sharper, GPIO.HIGH)
        else:
            GPIO.output(self.yellow_led_sharper, GPIO.LOW)

    
    def show_frequency_value(self, frequency):
        """Show the frequency value on the screen:
               - Display calculated analog value
        """
        # Display frequency
        self.display.update(frequency)
        
    
    
    def run(self):
        program                      = True
        while(1):
            
            if (program):
                
                from sound_analysis import frequency_value
                
                self.determine_LEDs(frequency_value)
                
                self.update_LEDs()
                
                self.show_frequency_value(frequency_value)
                
                time.sleep(5)
                
      
    
    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Set Display to something fun to show program is complete
        self.display.text("DEAD")
        self.display.set_colon(False)

        # Clean up GPIOs
        GPIO.output(self.yellow_led_flat, GPIO.LOW)
        GPIO.output(self.yellow_led_flater, GPIO.LOW)
        GPIO.output(self.yellow_led_sharp, GPIO.LOW)
        GPIO.output(self.yellow_led_sharper, GPIO.LOW)
        GPIO.output(self.green_led, GPIO.LOW)
        GPIO.output(self.blue_led_A, GPIO.LOW)
        GPIO.output(self.blue_led_B, GPIO.LOW)
        GPIO.output(self.blue_led_C, GPIO.LOW)
        GPIO.output(self.blue_led_D, GPIO.LOW)
        GPIO.output(self.blue_led_E, GPIO.LOW)
        GPIO.output(self.blue_led_F, GPIO.LOW)
        GPIO.output(self.blue_led_G, GPIO.LOW)

        # Clean up GPIOs
        GPIO.cleanup()

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the lock
    freq_detect = FrequencyDetector()

    try:
        # Run the code
        freq_detect.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        freq_detect.cleanup()

    print("Program Complete")