# HomeAssistantScripts

## 3dPrinterPowerCheck.py

This is a script I wrote to run after a job is sliced in prusa slicer using their "Post Processing Script" functionality detailed here:
https://help.prusa3d.com/article/post-processing-scripts_283913

This enables me to slice an object, and then immediately check to see if my printer is powered on and if it is not to turn it on

I power my RaspberryPi running octoprint off of a 24vdc to 5vdc USB buck converter so I cannot use most of the plugins for OctoPrint that would do this assuiming the server was running 24/7

My HomeAssistant instance is running 24/7 so I am able to use it for power monitoring and control of the smart switch that powers my Printer and Raspberry Pi
