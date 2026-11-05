BEFORE TO INSTALL RSLBOT
0) Install .NET8 runtime : https://dotnet.microsoft.com/en-us/download

HOW TO INSTALL RSLBOT USING RBDOWNLOAD.EXE
0) Download RBdownload.exe from Discord/RaidApp releases channel https://discord.com/channels/641849008913907722/1253687700691877940
1) Create a RSLBot folder
2) Move RBdownload.exe inside RSLBot folder
3) Run RBdownload.exe from RSLBot folder

HOW TO INSTALL RSLBOT FROM RSLBOT WEBSITE
0) Download the latest RSLBot version from https://community.rslbot.com/c/releases
1) Create a RSLBot folder
2) Unzip RSLBot version inside RSLBot folder
3) Run RBinstall.exe from RSLBot folder or just rename RaidBot.exe.new to RaidBot.exe

HOW TO ADD RSLBOT FOLDER TO ANTIVIRUS EXCLUSIONS TO AVOID FALSE POSITIVE ALERTS
✅ This prevents Windows Defender from scanning RSLBot folder:
0) Select the RSLBot folder path in Explorer and copy it in Clipboard (Ctrl C)
1) Press Win + X to Open Windows menu 
2) Select "Terminal (Admin)" or "Windows PowerShell (Admin)"
3) Type the following command: Add-MpPreference -ExclusionPath
4) Type " then Ctrl V then " to copy the RSLBot Path into the command
5) Press Enter to run the command
6) Verify that RSLBot folder has been added to Exclusions running command: Get-MpPreference | Select-Object -ExpandProperty ExclusionPath

HOW TO UNBLOCK RBDOWNLOAD, RBINSTALL AND RSLBOT FROM WINDOWS DEFENDER SMARTSCREEN
0) Right-click → Properties on the .exe file
1) Check Unblock if the option is available

HOW TO USE WITH PLARIUM PLAY
0) Put Windows Scale to 100% (Windows parameters/system/display) 
1) Download and install Plarium Play from https://plarium.com
4) Install Raid Shadow Legends in Plarium Play
5) Setup your account and set Raid game language to English
6) Verify in RSLBot folder that auth-crypto-x64.dll and RaidBot.exe have not been deleted by your Antivirus (add them to exclusions)
7) Start the Bot and let it resize Raid window
8) Stop the Bot
9) Close manually Raid
10) Let the Bot start Raid
11) Enjoy

HOW TO UPDATE RSLBOT WITH RBDOWNLOAD.EXE
0) Close manually Raid and Plarium Play
1) Start update of the Bot using RBdownload.exe in RSLBot folder or create a new folder to have a full installation keeping your old version
2) Verify in RSLBot folder that auth-crypto-x64.dll and RaidBot.exe have not been deleted by your Antivirus (add them to exclusions)
3) Let new version of Bot start Raid

HOW TO UPDATE PLARIUM PLAY
0) Close Bot before to update Plarium
1) Start Plarium and launch Raid manually
2) Start the Bot and let it resize Raid window
3) Stop the Bot
4) Close manually Raid
5) Let the Bot start Raid
