> This tool is used to catch the house sale information for '都会'.  
> Once double click dist/got_house_info.exe, chrome will fetch the data automatically then write them into house.xlsx

# Environment setup
- install chrome(Version 83.0.4103.116 (Official Build) (64-bit))
- install python3 
- pip install selenium
- pip install lxml
- pip install openpyxl
- pip install pyinstaller

# generate .exe
- pyinstaller -F --icon=favicon.ico got_house_info.py