# Initial import housekeeping
import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemeManager
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivy.metrics import dp
import threading
import subprocess
import socket
import time
import os
import math
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

# ---------------------------------------------------------------------------------------------------------------------------------------------
# 05/06/2024
# By Mason Stencel and Liam Hartman
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Misc Configuration Variables

developermode = 0           # set to 1 to disable all GPIO, temp probe, and obd stuff
externalshutdown = 0        # set to 1 if you have an external shutdown circuit applied - High = Awake, Low = Shutdown
AccelEnabled = 0            # set to 1 if adxl345 accelerometer is present
OBDEnabled = 1              # set to 1 if you have an OBD connection with the vehicle
onPi = 1                    # 1 by default, will change to 0 if code cannot import GPIO from Pi
autobrightness = 0          # AutoBrightness on Boot #set to 1 if you have the newer RPi display and want autobrightness
                            # Set to 2 for auto dim on boot every time (use main screen full screen button to toggle full dim and full bright)

# ---------------------------------------------------------------------------------------------------------------------------------------------
# For Resolution adjustments our 7 in display is 1024x600 resolution
from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')
from kivy.core.window import Window
Window.size = (1024, 600)

# ---------------------------------------------------------------------------------------------------------------------------------------------
# Inital Setup functions
try:
    import RPi.GPIO as GPIO
    onPi = 1  # If GPIO is successfully imported, we can assume we are running on a Raspberry Pi
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if externalshutdown == 1:
        GPIO.setup(21, GPIO.IN)  # setup GPIO pin #21 as external shutdown pin
except:
    onPi = 0
    externalshutdown = 0
    print("This is not being run on a Raspberry Pi. Functionality is limited.")

if onPi and OBDEnabled and developermode == 0:
    try:
        import obd
    except:
        OBDEnabled = 0
        print("OBD ERROR")
else:
    OBDEnabled = 0


# ---------------------------------------------------------------------------------------------------------------------------------------------
# Initialize Classes and Variables and threads
class sys:
    version = globalversion
    ip = "No IP address found..."
    ssid = "No SSID found..."
    getsysteminfo = False
    screen = 1
    shutdownflag = 0
    SpeedUnit = "MPH"
    
class OBD:
    Connected = 0  # connection is off by default - will be turned on in setup thread
    RPM_max = 0    # init all values to 0
    Speed_max = 0
    RPM = 0
    Speed = 0

    class dev:  # used for development of GUI and testing
        Speed = 0
        Speed_inc = 1
        RPM = 0
        RPM_inc = 1

    class enable:  # used to turn on and off OBD cmds to speed up communication
        RPM = 0
        Speed = 0

        def disableAll(obj):
            OBD.enable.RPM = 0
            OBD.enable.Speed = 0

    class warning:  # used to show warning when value is met, these will be read from savefile
        RPM = 0
        Speed = 0

    class gauge:  # Vars for gauge GUI

        class persegment:
            TimingAdv_max = 50
            RPM_max = 6100
            Speed_max = 129

            # Find value rounded to 2 decimal places
            RPM = round(RPM_max / 32.0, 2)

    # Thread functions
    # These will run in the background and will not block the GUI
    def OBD_setup_thread(self):
        global OBDEnabled
        try:
            os.system('sudo rfcomm bind /dev/rfcomm1 00:1D:A5:06:3C:2B')  
            print("RF Bind Complete")
        except:
            print("Failed to RF Bind - Device may already be connected?")
        time.sleep(2)
        try:
            OBD.connection = obd.OBD()  # auto-connects to USB or RF port
            OBD.cmd_RPM = obd.commands.RPM
            OBD.cmd_Speed = obd.commands.SPEED
            OBD.Connected = 1
            print("OBD System is Ready, Starting Update Thread")
        except:
            print("Error setting OBD vars. OBD is now disabled.")
            try:
                MainApp.show_warning(self,"Error setting OBD vars", "OBD is now disabled")
            except:
                print("Dialog could not open, no window?")
            OBDEnabled = 0

    def OBD_update_thread(self):
        while OBD.Connected == 0: # wait here while OBD system initializes
            pass
        while OBDEnabled and OBD.Connected:
            if OBD.enable.Speed:
                try:
                    response_SPEED = OBD.connection.query(OBD.cmd_Speed)  # send the command, and parse the response
                    if str(response_SPEED.value.magnitude) != 'None':  # only proceed if string value is not None
                        OBD.Speed = int(response_SPEED.value.magnitude * 0.6213711922) # Set int value
                        if OBD.Speed > OBD.Speed_max:  # set MAX variable if higher
                            OBD.Speed_max = OBD.Speed
                except:
                    print("Could not get OBD Response - Speed")

            if OBD.enable.RPM:
                try:
                    response_RPM = OBD.connection.query(OBD.cmd_RPM)
                    if str(response_RPM.value.magnitude) != 'None':
                        OBD.RPM = int(response_RPM.value.magnitude)
                        if OBD.RPM > OBD.RPM_max:
                            OBD.RPM_max = OBD.RPM
                except:
                    print("Could not get OBD Response - RPM")

    def start_setup_thread(self):
        OBDSetupThread = threading.Thread(name='obd_setup_thread', target=self.OBD_setup_thread)
        OBDSetupThread.start()

    def start_update_thread(self):
        OBDUpdateThread = threading.Thread(name='obd_update_thread', target=self.OBD_update_thread)
        OBDUpdateThread.start()

if OBDEnabled:
    OBD().start_setup_thread()
    OBD().start_update_thread()

# ---------------------------------------------------------------------------------------------------------------------------------------------
# Define Kivy Class

#MAIN SCREEN CLASS
class Gauge4Screen(Screen):
    pass
  
# ---------------------------------------------------------------------------------------------------------------------------------------------
# Main App Class
class MainApp(App):
    def build(self):
        Clock.schedule_interval(self.updatevariables, .1)
        Clock.schedule_interval(self.updateOBDdata, .01)
# ---------------------------------------------------------------------------------------------------------------------------------------------
    version = StringProperty()
    TempUnit = StringProperty()
    SpeedUnit = StringProperty()

    Redline = NumericProperty(0)
    SpeedLimit = NumericProperty(0)

    Speed = NumericProperty(0)
    Speed_max = NumericProperty(0)
    RPM = NumericProperty(0)
    RPM_max = NumericProperty(0)

    RPMWarn = NumericProperty(0)
    SpeedWarn = NumericProperty(0)

    RPM_Image = StringProperty()

    RPMGaugeMax = OBD.gauge.persegment.RPM_max
    SpeedGaugeMax = OBD.gauge.persegment.Speed_max

    def updatevariables(self, *args):
        self.version = sys.version
        self.SpeedUnit = sys.SpeedUnit
        self.shutdownflag = sys.shutdownflag
        self.RPMWarn = OBD.warning.RPM
        self.SpeedWarn = OBD.warning.Speed
        if sys.getsysteminfo == True:
            self.get_CPU_info()
            self.get_IP()

    def updateOBDdata(self, *args):
        if OBD.Connected and developermode == 0:
            try:
                self.Speed = OBD.Speed
                self.Speed_max = OBD.Speed_max
                self.RPM = OBD.RPM
                self.RPM_max = OBD.RPM_max
            except:
                print("Python -> Kivy OBD Var Setting Failure")

# ---------------------------------------------------------------------------------------------------------------------------------------------
# Scheduling Functions
    def toggleSpeedUnit(self):
        if sys.SpeedUnit == "KPH":
            sys.SpeedUnit = "MPH"
        else:
            sys.SpeedUnit = "KPH"

    def zero_out_max(obj):  # zeros out RPM max
        OBD.RPM_max = 0
        OBD.Speed_max = 0

    def OBDEnabler(obj, PID, status):
        setattr(OBD.enable, PID, status)  # sets OBD enable class based on PID (text) and Status (int) input

    def OBDOFF(obj):
        OBD.enable.RPM = 0
        OBD.enable.Speed = 0

    def initOBD(self):
        global OBDEnabled
        OBDEnabled = 1
        OBD().OBD_setup_thread()  # retry OBD setup thread
        
# ---------------------------------------------------------------------------------------------------------------------------------------------
if __name__ =='__main__':
    MainApp().run()
