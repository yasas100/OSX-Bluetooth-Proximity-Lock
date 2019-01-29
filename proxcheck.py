import sys
from termcolor import colored
from optparse import OptionParser
from os import path
from time import sleep
from IOBluetooth import *
from IOBluetoothUI import *
from ctypes import CDLL

def logoff():
    print("Logging Off")
    loginPF = CDLL('/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
    result = loginPF.SACLockScreenImmediate()


opts = OptionParser()
opts.add_option('-d', '--device', dest='device', help='ask for device', default=False, action='store_true')
(options, args) = opts.parse_args()

if path.exists('device.conf') and not options.device:
    with open('device.conf', 'r') as devFile:
        devAddr = devFile.read()
        dev = IOBluetoothDevice.deviceWithAddressString_(devAddr)
else:
    with open('device.conf', 'w') as devFile:
        selector = IOBluetoothDeviceSelectorController.deviceSelector()
        selector.runModal()
        results = selector.getResults()
        dev = results[0]
        devAddr = dev.getAddressString()
        devFile.write(devAddr)

dev.openConnection()
if dev.isConnected():
    print("Device Connected")
    while True:
        if not dev.isConnected():
            dev.openConnection()
        devSignal = dev.rawRSSI()
        print(devSignal)
        #if devSignal < 0 and devSignal > -60:
        # color = 'green'
        #else:
        #   color = 'red'
        if devSignal < -50:
            logoff()
        sys.stdout.write("%s\r" % devSignal)
        sys.stdout.flush()
        sleep(1)

