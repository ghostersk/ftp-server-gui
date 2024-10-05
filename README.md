# Simple FTP Server with GUI (prefferably for windows)
- option to choose what folder is served by the server
- option to select port ( ports bellow 1024 require permissions, unless already allowed )
- simple authentication - default is: user   123
- with system tray icon to restore daemon FTP server after is minimized
- it can run in background from launch if you set `run_as_daemon = 1` in `ftp-config.cfg`
- simple connection from Explorer: `ftp://user:123@192.168.1.5` to access hosted files in RW mode

#### Default values for `ftp-config.cfg`
```
[FTP]
username = user
password = 123
port = 21
ftp_directory = C:\Temp\FTP
run_as_daemon = 0
log_file = ftp_log.txt
```

#### Requirements:
```
PyQt5
pyftpdlib

# for windows compiling:
pyinstaller
Pillow # optional if you do not use .ico file but other image format
```

### Windows:
- This was built for windows, as currently there is no simple non install FTP Server solution.
- On windows you do not need admin rights, only to allow traffic on ports <1024 through windows firewall
- You can select FTP folder location ( for now the config is not being saved after change in GUI )
- it keeps logged access in file

### Linux:
- It works on linux too, but for now you can run only ports 1024+ or you need to run it with sudo
- It also creates the folder from where it is run "C:\Temp\FTP" or the folder in cfg file
- Also on Linux it does not quit with buttons when FTP started, it must be killed, or `ctrl+c` when opened from terminal

### Windows building is simple as:
`pyinstaller --onefile --windowed --add-data "ftp.png;." --icon=ftp.png ftp_gui.py`

![image](https://github.com/user-attachments/assets/b23c8caf-6eb2-49b3-87ea-bd0dcb0edb31)

### Issues:
1. Quit from system tray does not work when daemon mod is ON
2. Settings are not saved when changed in GUI to config, this would need to be changed prior starting the app
3. The app works ok on Windows  but for linux it has few flaws
   - it creates folder "C:\Temp\FTP" in current directory if there is not other linux location in `ftp-config.cfg` already
   - it would require sudo to run on ports <1024 or you need to allow non sudo users to use port 21 ( port can be changed)
   - when the app is started as daemon it will not be stopped from gui, it must be killed

##### contribution:
FTP.png icon: <a href="https://www.flaticon.com/free-icons/ftp" title="ftp icons">Ftp icons created by andinur - Flaticon</a>
