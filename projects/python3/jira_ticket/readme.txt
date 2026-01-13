1. access below jira link: https://jira.sw.nxp.com/issues/?jql=project%20%3D%20ACSVS%20AND%20affectedVersion%20%3D%20i.mxRT2660%20ORDER%20BY%20priority%20DESC%2C%20updated%20DESC
2. Press F12 to check the source code of this website 
3. extend "Export" and click "Select an element" in the left top of source code. Click the Excel CSV(All fields) to get the CSV source link address
4. Right click the source code to copy the link address. Store it in the config.ymal
5. # generate .exe
- pyinstaller -F --icon=favicon.ico jira_ve_ticket.py