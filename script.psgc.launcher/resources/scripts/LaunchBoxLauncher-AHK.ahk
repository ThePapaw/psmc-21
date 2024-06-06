;PSGC LaunchBox launcher for PSMC
;Developer: The Papaw
;See: https://github.com/ThePapaw/psmc-19
;Based on autohotkey script by teeedubb
;See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
;Originally modded for LaunchBox by ashramrak;CoinTos
;See: http://forums.launchbox-app.com/topic/28804-kodi-addon-for-launching-big-box/?do=findComment&comment=169254
;
;Manual script usage: LaunchBoxLauncher-AHK.ahk "e:\path\to\LaunchBox.exe" "0/1" "true/false" "scriptpath/false" "scriptpath/false" "PSMCpath/false" "true/false" "0/<drive letter>:"
;$2 = 0 Quit PSMC, 1 Minimize PSMC. $3 = PSMC portable mode. $4 = pre script. $5 = post script. $6 = PSMC path to override detect, $7 = Hide Taskbar $8 = Mapped drive
;Change the 'llsrevision=' number below to 999 to preserve changes through addon updates, otherwise it shall be overwritten.
;
llsrevision=107

#NoEnv  
#SingleInstance force
SetWorkingDir %A_ScriptDir%

; HideShowTaskbar function posted by teadrinker on AHK Forums
HideShowTaskbar(action) {
   static ABM_SETSTATE := 0xA, ABS_AUTOHIDE := 0x1, ABS_ALWAYSONTOP := 0x2
   VarSetCapacity(APPBARDATA, size := 2*A_PtrSize + 2*4 + 16 + A_PtrSize, 0)
   NumPut(size, APPBARDATA), NumPut(WinExist("ahk_class Shell_TrayWnd"), APPBARDATA, A_PtrSize)
   NumPut(action ? ABS_AUTOHIDE : ABS_ALWAYSONTOP, APPBARDATA, size - A_PtrSize)
   DllCall("Shell32\SHAppBarMessage", UInt, ABM_SETSTATE, Ptr, &APPBARDATA)
}
; Move and center window on selected monitoring
MoveCenterOnMonitor(WinTitle, WinText, ScrnH, ScrnW, ScrnX, ScrnY) {
    H = %ScrnH%
    W = %ScrnW%
    X = %ScrnX%
    Y = %ScrnY%
    WinGetPos,,, Width, Height, %WinTitle%, %WinText%
    WinMove, %WinTitle%, %WinText%, X+(W/2)-(Width/2), Y+(H/2)-(Height/2)
    WinActivate, %WinTitle%, %WinText%
}

; Set script tray icon
if FileExist("LaunchBoxLauncher-AHK.ico")
    Menu, Tray, Icon, LaunchBoxLauncher-AHK.ico

; Set number of arguments
ArgNum = %0%

; Check for arguments
if (ArgNum != 8)
{
    MsgBox, 16, Error, This script requires all arguments to be supplied but only received %ArgNum%. See script file for details.
    ExitApp
}

; Set each arguments to variable
LaunchBox = %1%
HandlePSMC = %2%
PSMCPortable = %3%
PreScript = %4%
PostScript = %5%
PSMCOverride = %6%
HideTaskbar = %7%
MappedDrive = %8%

; Set Launchbox root directory
SplitPath, LaunchBox,, BaseDir

; Start Logging
if FileExist("LaunchBoxLauncher.log")
{
    FileMove, LaunchBoxLauncher.log, LaunchBoxLauncher.old.log, 1
    FileDelete, LaunchBoxLauncher.log
}
FileAppend, LaunchBoxLauncher Log `n, LaunchBoxLauncher.log
FileAppend, --------------------- `n, LaunchBoxLauncher.log
FileAppend, %A_Now% - INFO: Starting LaunchBox Launcher Autohotkey script revision %llsrevision%. `n, LaunchBoxLauncher.log

; Detect PSMC path and executable or use override
if (PSMCOverride = "false")
{
    FileAppend, %A_Now% - INFO: Detecting PSMC information. `n, LaunchBoxLauncher.log
    WinGet, PSMCExe, ProcessPath, ahk_class PSMC
    if (!PSMCExe)
    {
        FileAppend, %A_Now% - ERROR: Failed to detect PSMC executable information. `n, LaunchBox.log
        LLRunFailed := 1
    }
    FileAppend, %A_Now% - INFO: Detected PSMC running at "%PSMCExe%". `n, LaunchBoxLauncher.log
}
else
{
    ; Using PSMC path override
    PSMCExe := PSMCOverride
    FileAppend, %A_Now% - INFO: Using override path for PSMC "%PSMCExe%". `n, LaunchBoxLauncher.log
}

;Hide Taskbar Ckeck
if (HideTaskbar != "false")
{
    FileAppend, %A_Now% - INFO: Hiding Taskbar. `n, LaunchBoxLauncher.log
    HideShowTaskbar(true)
}

; Check for Pre-script
if (PreScript != "false")
{
    FileAppend, %A_Now% - INFO: Running Pre-script. `n, LaunchBoxLauncher.log
    RunWait, %Prescript%,,Hide UseErrorLevel
    if ErrorLevel
        FileAppend,
        (
        %A_Now% - WARNING: %Prescript% exited with an error. Please check your script/program for errors or if this is batch file please add exit 0 to the end of the batch script to remove this warning. `n
        ), LaunchBoxLauncher.log
    FileAppend, %A_Now% - INFO: Running Pre-script completed. `n, LaunchBoxLauncher.log
}

; Detect Monitors and figure out which monitor PSMC is running on
SysGet, MonitorCount, 80
FileAppend, %A_Now% - INFO: Monitor Count: %MonitorCount%. `n, LaunchBoxLauncher.log
if (MonitorCount > 1)
{
    WinGetPos, PSMCX, PSMCY, PSMCW, PSMCH, ahk_class PSMC
    WinGet, PSMCState, MinMax, ahk_class PSMC
    PSMCCenterX := PSMCX+(PSMCW/2)
    PSMCCenterY := PSMCY+(PSMCH/2)
    FileAppend, %A_Now% - INFO: PSMC detected at X%PSMCX% Y%PSMCY%. `n, LaunchBoxLauncher.log
    Loop, %MonitorCount%
    {
        SysGet, Monitor, Monitor, %A_Index%
        SysGet, MonitorWorkArea, MonitorWorkArea, %A_Index%
        if (MonitorLeft <= PSMCCenterX and MonitorTop <= PSMCCenterY and MonitorRight >= PSMCCenterX and MonitorBottom >= PSMCCenterY)
        {
            ScrHeight := MonitorBottom - MonitorTop
            ScrWidth := MonitorRight - MonitorLeft
            ScrX := MonitorLeft
            ScrY := MonitorTop
            ScrWHeight := MonitorWorkAreaBottom - MonitorWorkAreaTop
            ScrWWidth := MonitorWorkAreaRight - MonitorWorkAreaLeft
            ScrWX := MonitorWorkAreaLeft
            ScrWY := MonitorWorkAreaTop
            FileAppend, %A_Now% - INFO: Monitor %A_Index% selected. `n, LaunchBoxLauncher.log
            break
        }
    }
}
else
{
    SysGet, MonitorPrimary, MonitorPrimary
    SysGet, MonitorWorkArea, MonitorWorkArea, %MonitorPrimary%
    ScrHeight := A_ScreenHeight
    ScrWidth := A_ScreenWidth
    ScrX := 0
    ScrY := 0
    ScrWHeight := MonitorWorkAreaBottom - MonitorWorkAreaTop
    ScrWWidth := MonitorWorkAreaRight - MonitorWorkAreaLeft
    ScrWX := MonitorWorkAreaLeft
    ScrWY := MonitorWorkAreaTop
}

; Load Blank GUI
FileAppend, %A_Now% - INFO: Loading blank gui at W%ScrWidth% H%ScrHeight% X%ScrX% Y%ScrY%. `n, LaunchBoxLauncher.log
Gui,Color,Black,000000
Gui, -Caption -dpiscale
Gui,Show, W%ScrWidth% H%ScrHeight% X%ScrX% Y%ScrY%

; Start Run procedures
FileAppend, %A_Now% - INFO: Starting all LaunchBox procedures. `n, LaunchBoxLauncher.log

FileAppend, %A_Now% - INFO: Attempting to run "%LaunchBox%". `n, LaunchBoxLauncher.log
Run, %LaunchBox%,,UseErrorLevel
if ErrorLevel
{
    FileAppend, %A_Now% - ERROR: %LaunchBox% failed to run. `n, LaunchBoxLauncher.log
    LLRunFailed := 1
}
else
{
    FileAppend, %A_Now% - INFO: LaunchBox run successful. LaunchBox is starting up. `n, LaunchBoxLauncher.log

    ; Wait for LaunchBox to run
    Process, Wait, LaunchBox.exe, 60
    if (ErrorLevel = 0)
    {
        FileAppend, %A_Now% - ERROR: Failed to detect LaunchBox in 60 seconds. Aborting. `n, LaunchBoxLauncher.log
        LLRunFailed := 1
    }
    else
    {
        FileAppend, %A_Now% - INFO: Process detected. LaunchBox.exe is running. `n, LaunchBoxLauncher.log
        ; Loading loop in case of error
        Loop
        {
        Process, Exist, LaunchBox.exe
            NewPID := ErrorLevel
            if (NewPID = 0)
            {
                FileAppend, %A_Now% - ERROR: LaunchBox.exe is gone. Aborting. `n, LaunchBoxLauncher.log
                LLRunFailed := 1
                break
            }
            else
            {
                if WinExist("ahk_exe LaunchBox.exe")
                    break
                else
                    continue
            }
            Sleep, 500
        }
    }
}

; LaunchBox run error check
if !LLRunFailed
{
    Startup := 1
    PastFullFilename := ""
    ; Check if we need to minimise or close PSMC
    FileAppend, %A_Now% - INFO: Minimizing or exiting PSMC..., LaunchBoxLauncher.log
    if HandlePSMC
        WinMinimize, ahk_class PSMC
    else
    {
        Run, %comspec% /c taskkill /im PSMC.exe,,Hide
        Run, %comspec% /c timeout /t 1 && tasklist /nh /fi "imagename eq PSMC.exe" | find /i "PSMC.exe" >nul && (taskkill /f /im PSMC.exe),,Hide
    }
    FileAppend, Done. `n, LaunchBoxLauncher.log

    ; Main loop to monitor if LaunchBox has been exited and if an update was found
    FileAppend, %A_Now% - INFO: Starting LaunchBox monitoring. `n, LaunchBoxLauncher.log
    Loop
    {
        if (Startup = 1)
        {
            FileAppend, %A_Now% - INFO: Entering start up process. `n, LaunchBoxLauncher.log
            ; LaunchBox move handling loop
            Loop
            {
                ; Ignore and move the loading screen
                if WinExist("ahk_exe LaunchBox.exe","Version")
                {
                    FileAppend, %A_Now% - INFO: Launchbox loading screen detected. Waiting for it to close..., LaunchBoxLauncher.log
                    if (MonitorCount > 1)
                        MoveCenterOnMonitor("LaunchBox ahk_exe LaunchBox.exe", "Version", ScrHeight, ScrWidth, ScrX, ScrY)
                    WinWaitClose, ahk_exe LaunchBox.exe, Version
                    FileAppend, Done. `n, LaunchBoxLauncher.log
                }
    
                WinWait, LaunchBox ahk_exe LaunchBox.exe,,30

                ; Wait for classic Update window to close if detected
                if WinExist("LaunchBox ahk_class #32770")
                {
                    FileAppend, %A_Now% - INFO: LaunchBox upgrade pop up detected. Waiting for it to close..., LaunchBoxLauncher.log
                    if (MonitorCount > 1)
                        MoveCenterOnMonitor("LaunchBox ahk_class #32770","", ScrHeight, ScrWidth, ScrX, ScrY)
                    WinWaitClose, LaunchBox ahk_class #32770
                    FileAppend, Done. `n, LaunchBoxLauncher.log
                }

                ; Wait for downloading update window to close if detected
                if WinExist("Downloading ahk_exe LaunchBox.exe")
                {
                    FileAppend, %A_Now% - INFO: Upgrade downloading pop up detected. Waiting for it to close..., LaunchBoxLauncher.log
                    WinWaitClose, Downloading ahk_exe LaunchBox.exe
                    FileAppend, Done. `n, LaunchBoxLauncher.log
                    break
                }
                
                ; Close Welcome window if open
                if WinExist("Welcome to LaunchBox ahk_exe LaunchBox.exe") and !WinExist("LaunchBox ahk_class #32770")
                    WinClose, Welcome to LaunchBox ahk_exe LaunchBox.exe

                WinGetClass, LaunchBoxClass, LaunchBox ahk_exe LaunchBox.exe,,LaunchBox ahk_class #32770
                WinGet, LaunchBoxState, MinMax, ahk_class %LaunchBoxClass%
                WinGetPos, LaunchBoxX, LaunchBoxY, LaunchBoxW, LaunchBoxH, ahk_class %LaunchBoxClass%

                ; Wait for Update alert window to close if detected
                if (LaunchBoxW <= 600 and LaunchBoxH <= 260)
                {
                    FileAppend, %A_Now% - INFO: Launchbox upgrade pop up detected. Waiting for it to close..., LaunchBoxLauncher.log
                    if (MonitorCount > 1)
                        MoveCenterOnMonitor("ahk_class" LaunchBoxClass,"", ScrHeight, ScrWidth, ScrX, ScrY)
                    WinWaitClose, ahk_class %LaunchboxClass%
                   FileAppend, Done. `n, LaunchBoxLauncher.log
                }
                
                ; Check if there is no upgrade window and LaunchBox is not maximized and in the right position
                if ((LaunchBoxX != ScrX or LaunchBoxY != ScrY or LaunchBoxW < ScrWWidth or LaunchBoxY < ScrWHeight) and (LaunchBoxW > 600 and LaunchBoxH > 260))
                {
                    if (LaunchBoxState = -1 or LaunchBoxState = 1)
                        WinRestore, ahk_class %LaunchBoxClass%
                    WinMove, ahk_class %LaunchBoxClass%,, ScrX, ScrY
                    WinMaximize, ahk_class %LaunchBoxClass%
                    WinActivate, ahk_class %LaunchBoxClass%
                }
                
                ; Check if everything is good and break the loop
                if (LaunchBoxX = ScrX and LaunchBoxY = ScrY and LaunchBoxState = 1 and !WinExist("Welcome to LaunchBox ahk_exe LaunchBox.exe") and !WinExist("LaunchBox ahk_class #32770") and !WinExist("Downloading ahk_exe LaunchBox.exe"))
                {
                    FileAppend, %A_Now% - INFO: Start up completed successfully. `n, LaunchBoxLauncher.log
                    break
                }
            }
            Startup := 0
        }
        ; Check if LaunchBox is behind blank window
        if WinActive("LaunchBoxLauncher-AHK.ahk") and WinExist("ahk_class" LaunchBoxClass)
            WinActivate, ahk_class %LaunchBoxClass%

        ; Check if LaunchBox is closed
        if !WinExist("ahk_class" LaunchBoxClass)
        {
            ; Check if upgrade loop needs to be skipped
            if !SkipUpgrade
            {
                ; Initiate required update variables
                UpdateDir := BaseDir "\Updates"
                FullFilename := ""
                PastTime :=
                PastTime += -1, minutes
            
                ; Scan update folder for a file that was modified in the last minute
                Loop, Files, %UpdateDir%\*.exe
                {
                    if (A_LoopFileTimeModified > PastTime)
                    {
                        PastTime := A_LoopFileTimeModified
                        FullFilename := A_LoopFileName
                    }
                }

                ; Check if the scan found an update filename to monitor
                if (FullFilename != "" and PastFullFilename != FullFilename)
                {
                    PastFullFilename := FullFilename
                    StringTrimRight, Filename, FullFilename, 4
                    FileAppend, %A_Now% - INFO: Update file %FullFilename% found. Starting Update monitoring. `n, LaunchBoxLauncher.log

                    ; Wait for Updater to run
                    Process, Wait, %Filename%.tmp, 60
                    if (ErrorLevel = 0)
                    {
                        FileAppend, %A_Now% - ERROR: Failed to detect Updater in 60 seconds. Aborting. `n, LaunchBoxLauncher.log
                        UpdateAbort := 1
                    }
                    else
                    {                        
                        ; Loading loop in case of error
                        Loop
                        {
                            Process, Exist, %Filename%.tmp
                            NewPID := ErrorLevel
                            if (NewPID = 0)
                            {
                                FileAppend, %A_Now% - ERROR: Updater is gone. Aborting. `n, LaunchBoxLauncher.log
                                UpdateAbort := 1
                                break
                            }
                            else
                            {
                                if WinExist("ahk_exe " Filename ".tmp")
                                {
                                    WinWaitActive, Setup - LaunchBox,, 10
                                    if (MonitorCount > 1)
                                        MoveCenterOnMonitor("Setup - LaunchBox","", ScrHeight, ScrWidth, ScrX, ScrY)
                                    break
                                }
                                else
                                    continue
                            }
                            Sleep, 500
                        }
                    }

                    ; Start update monitoring loop
                    Loop
                    {
                        ; Check for main installer window
                        if WinExist("Setup - LaunchBox")
                            continue
                        else
                        {
                            ; Check for the process still running error message and attempt to correct it
                            if WinExist("Setup ahk_class #32770")
                            {
                                Process, WaitClose, LaunchBox.exe, 2
                                if ErrorLevel
                                {
                                    Run, %comspec% /c taskkill /im LaunchBox.exe,,Hide
                                    Run, %comspec% /c timeout /t 1 && tasklist /nh /fi "imagename eq LaunchBox.exe" | find /i "LaunchBox.exe" >nul && (taskkill /f /im LaunchBox.exe),,Hide
                                }
                                else
                                {
                                    WinActivate, Setup ahk_class #32770
                                    Send {Enter}
                                    Sleep, 1000
                                }
                            }
                            else if UpdateAbort
                            {
                                SkipUpdate := 1
                                break
                            }
                            else
                            {
                                Process, Wait, LaunchBox.exe, 60
                                if (ErrorLevel = 0)
                                {
                                    FileAppend, %A_Now% - WARNING: LaunchBox failed to relaunch within 60 seconds after installer closed. Update might have failed. `n, LaunchBoxLauncher.log
                                    SkipUpgrade := 1
                                    break
                                }
                                else
                                {
                                    WinWaitActive, ahk_exe LaunchBox.exe,, 5
                                    Startup := 1
                                    FileAppend, %A_Now% - INFO: Update is complete. Finished Update monitoring. `n, LaunchBoxLauncher.log
                                    break
                                }
                            }
                        }
                        Sleep, 500
                    }
                }
                else
                    break
            }
            else
                break
        }
        Sleep, 500
    }
    FileAppend, %A_Now% - INFO: LaunchBox monitoring completed. `n, LaunchBoxLauncher.log
}
FileAppend, %A_Now% - INFO: All LaunchBox procedures completed. `n, LaunchBoxLauncher.log

; Check for a Post-script
if (PostScript != "false")
{
    FileAppend, %A_Now% - INFO: Running Post-script. `n, LaunchBoxLauncher.log
    RunWait, %PostScript%,,Hide UseErrorLevel
    if ErrorLevel
        FileAppend, 
        (
        %A_Now% - WARNING: %PostScript% exited with an error. Please check your script/program for errors or if this is batch file please add exit 0 to the end of the batch script to remove this warning. `n
        ), LaunchBoxLauncher.log
    FileAppend, %A_Now% - INFO: Running Post-script completed. `n, LaunchBoxLauncher.log
}

; LaunchBox run error check
if !LLRunFailed
{
    ; Check to see if PSMC is minimised or needs to be restarted
    FileAppend, %A_Now% - INFO: Maximizing or restarting PSMC..., LaunchBoxLauncher.log
    if HandlePSMC
    {
        if (PSMCState = 1)
            WinMaximize, ahk_class PSMC
        else
            WinRestore, ahk_class PSMC
    }
    else
    {
        ; Check if we need to run PSMC in portable mode
        if (PSMCPortable = "true")
        {
            Run, %PSMCExe% -p,,UseErrorLevel
            if ErrorLevel
                Run, %comspec% /c "Start PSMC:",,Hide
        }
        else
        {
            Run, %PSMCExe%,,UseErrorLevel
            if ErrorLevel
                Run, %comspec% /c "Start PSMC:",,Hide
        }
    }
    FileAppend, Done. `n, LaunchBoxLauncher.log
}

WinWait, ahk_class PSMC,,60
if Errorlevel
    FileAppend, %A_Now% - ERROR: Failed to detect PSMC in 60 seconds. Aborting. `n, LaunchBoxLauncher.log
else
{
    WinActivate, ahk_class PSMC
    WinWaitActive, ahk_class PSMC
    FileAppend, %A_Now% - INFO: PSMC is now active. `n, LaunchBoxLauncher.log
}

; Restore Taskbar check
if (HideTaskbar != "false")
{
    FileAppend, %A_Now% - INFO: Restoring Taskbar. `n, LaunchBoxLauncher.log
    HideShowTaskbar(false)
}

; Destroy mapped drive
if (MappedDrive != 0)
{
    Sleep, 5000
    Run, %comspec% /c net use %MappedDrive% /delete /y,,Hide
    FileAppend, %A_Now% - INFO: Removing Mapped Drive %MappedDrive%. `n, LaunchBoxLauncher.log
}
; End logging
FileAppend, %A_Now% - INFO: Exiting LaunchBox Launcher Autohotkey script. `n, LaunchBoxLauncher.log
ExitApp