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
py C:\Users\user\Desktop\ssm-master\reformatter.py -f C:\Users\user\Downloads\159313-Locations.csv
```
or
```
py "C:\Users\Neil Hammerschlag\Desktop\SSM\reformatter.py" -f "C:\Users\Neil Hammerschlag\Desktop\SSM\175440-Locations.csv" -a "C:\Users\Neil Hammerschlag\Desktop\SSM\start_data.csv"
```
The "-f" flag tells the code where the input file the user wishes to filter is stored

The "-a" flag tells the code where to find the .csv file containing the start date/time meta data. If this flag is not 
used, All values (After Jan 1, 1970 00:00:00) will be used in the analysis. 
This file should be formatted as two (2) coulumns without headers. The first column should be a list of ID numbers and the second 
column should be their corresponding start datetimes in the format YYYY-MM-DDTHH:MM:SS (i.e., 2019-04-23T00:00:00).

An example of the table would look like:

| 11111 | 2017-04-18T00:00:00 |
|-------|---------------------|
| 22222 | 2015-11-05T12:30:47 

**NOTE: This file can be named anything as long as it is saved as a plain .csv file (e.g., "my_start_data.csv"). No Encodings (e.g., UTF-8)

The "-g" flag tells the code the maximum gap you wish to use. If the "-g" flag is not used, the default value is 14 days.
An example using a 5 day gap is as follows:
```
py "C:\Users\Neil Hammerschlag\Desktop\SSM\reformatter.py" -f "C:\Users\Neil Hammerschlag\Desktop\SSM\175440-Locations.csv" -a 2017-04-18T00:00:00 -g 5d
```
A file will be generated and placed in the same directory as the raw data. This file will be named something like 
"159313-Locations_formatted.txt"

####Notes:
- py is the command to have the script be read and executed by python
- You will need to know the datetime the tag went into service

### Output
The output file should be able to be input into the R based SSM tool. 


