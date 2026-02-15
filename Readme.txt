BEFORE TO INSTALL RAIDBOT
0) Install .NET8 runtime : https://dotnet.microsoft.com/en-us/download

HOW TO INSTALL RAIDBOT USING RBDOWNLOAD.EXE
0) Download RBdownload.exe from Discord/RaidApp releases channel https://discord.com/channels/641849008913907722/1253687700691877940
1) Create a RaidBot folder
2) Move RBdownload.exe inside RaidBot folder
3) Run RBdownload.exe from RaidBot folder

HOW TO INSTALL RAIDBOT FROM RAIDBOT WEBSITE
0) Download last RaidBot version from raidbot.app https://community.raidbot.app/index.php?/forum/3-raidbot-releases/
1) Create a RaidBot folder
2) Unzip RaidBot version inside RaidBot folder
3) Run RBinstall.exe from RaidBot folder or just rename RaidBot.exe.new to RaidBot.exe

HOW TO ADD RAIDBOT FOLDER TO ANTIVIRUS EXCLUSIONS TO AVOID FALSE POSITIVE ALERTS
✅ This prevents Windows Defender from scanning RaidBot folder:
0) Select the RaidBot folder path in Explorer and copy it in Clipboard (Ctrl C)
1) Press Win + X to Open Windows menu 
2) Select "Terminal (Admin)" or "Windows PowerShell (Admin)"
3) Type the following command: Add-MpPreference -ExclusionPath
4) Type " then Ctrl V then " to copy the RaidBot Path into the command
5) Press Enter to run the command
6) Verify that RaidBot folder has been added to Exclusions running command: Get-MpPreference | Select-Object -ExpandProperty ExclusionPath

HOW TO UNBLOCK RBDOWNLOAD, RBINSTALL AND RAIDBOT FROM WINDOWS DEFENDER SMARTSCREEN
0) Right-click → Properties on the .exe file
1) Check Unblock if the option is available

HOW TO USE WITH PLARIUM PLAY
0) Put Windows Scale to 100% (Windows parameters/system/display) 
1) Download and install Plarium Play from https://plarium.com
4) Install Raid Shadow Legends in Plarium Play
5) Setup your account and set Raid game language to English
6) Verify in RaidBot folder that auth-crypto.dll, auth-crypto-x64.dll and RaidBot.exe have not been deleted by your Antivirus (add them to exclusions)
7) Start the Bot and let it resize Raid window
8) Stop the Bot
9) Close manually Raid
10) Let the Bot start Raid
11) Enjoy

HOW TO UPDATE RAIDBOT WITH RBDOWNLOAD.EXE
0) Close manually BlueStacks and Plarium
1) Start update of the Bot using RBdownload.exe in RaidBot folder or create a new folder to have a full installation keeping your old version
2) Verify in RaidBot folder that auth-crypto.dll, auth-crypto-x64.dll and RaidBot.exe have not been deleted by your Antivirus (add them to exclusions)
3) Let new version of Bot start BlueStacks or Plarium

HOW TO UPDATE PLARIUM PLAY
0) Close Bot before to update Plarium
1) Start Plarium and launch Raid manually
2) Start the Bot and let it resize Raid window
3) Stop the Bot
4) Close manually Raid
5) Let the Bot start Raid