# ssm
This code package is designed to eliminate the manual labor of formatting and filtering shark tag data downloaded from 
Wildlife Computers. This Data will be prepared for track analysis by the R package SSM. Below we will describe the 
process of installing this package and running this package.

### Python Installation
1) Navigate to: 
https://www.python.org/downloads/windows/
2) Select the latest python 3 release (should be at the top of the page)
3) Scroll to the bottom and select either Windows x86-64 executable installer for 64-bit or Windows x86 executable 
installer for 32-bit (most likely you have a 64 bit machine)
4) Run the Installer and be sure to check the box that says "Add Python3.X to PATH"
5) Click "Install Now"

### Download Reformatter
1) Navigate to:
https://github.com/L2Platforms/ssm
2) Ensure the Branch is set to "master"
3) Click the green "Clone or download" button
4) Click "Download ZIP" button
5) Extract the zip contents to a location of your choosing

**NOTE: This process will change once the repository is made private

### Run Reformatter.py
1) Open up a Command Prompt from start menu (type command prompt at start menu)
2) You will need to know where your version of the reformatter code resides and where your data raw data resides. 
For example, run:
```
py C:\Users\user\Desktop\ssm-master\reformatter.py -f C:\Users\user\Downloads\159313-Locations.csv -a 2016-10-18T14:22:33
```
or
```
py "C:\Users\Neil Hammerschlag\Desktop\SSM\reformatter.py" -f "C:\Users\Neil Hammerschlag\Desktop\SSM\175440-Locations.csv" -a 2017-04-18T00:00:00
```
3) A file will be generated and placed in the same directory as the raw data. This file will be named something like 
"159313-Locations_formatted.txt"

####Notes:
- py is the command to have the script be read and executed by python
- You will need to know the datetime the tag went into service

### Output
The output file should be able to be input into the R based SSM tool. 


