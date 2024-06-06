;PSGC BigBox Launcher for PSMC
;Developer: The Papaw
;See: https://github.com/ThePapaw/psmc-19
;Based on autohotkey script by teeedubb
;See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
;Originally modded for LaunchBox by ashramrak;CoinTos
;See: http://forums.launchbox-app.com/topic/28804-kodi-addon-for-launching-big-box/?do=findComment&comment=169254
;
;Manual script usage: LaunchBoxLauncher-AHK.ahk "e:\path\to\bigbox.exe" "0/1" "true/false" "scriptpath/false" "scriptpath/false" "psmcpath/false" "true/false" "0/<drive letter>:"
;$2 = 0 Quit PSMC, 1 Minimize PSMC. $3 = PSMC portable mode. $4 = pre script. $5 = post script. $6 = PSMC path to override detect, $7 = Hide Taskbar $8 = Mapped drive
;Change the 'llsrevision=' number below to 999 to preserve changes through addon updates, otherwise it shall be overwritten.
;
llsrevision=105

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

; Modified from show/hide the mouse systems cursor function posted by wolf_II on AHK Forums
ShowBusy(bShow := True) {
    static BlankCursor
    static BusyCursor = 32514
    local ANDmask, XORmask, CursorHandle

    ; Shortcut for showing the mouse cursor
    if bShow
        Return, DllCall("SystemParametersInfo", "UInt", 0x57, "UInt", 0, "Ptr",  0, "UInt", 0)

    ; Create BlankCursor only once
    if Not BlankCursor
    {
        VarSetCapacity(ANDmask, 32 * 4, 0xFF)
        VarSetCapacity(XORmask, 32 * 4, 0x00)

        BlankCursor := DllCall("CreateCursor", "Ptr", 0, "Int", 0, "Int", 0, "Int", 32, "Int", 32, "Ptr", &ANDmask, "Ptr", &XORmask)
    }

    ; Set system Busy to Blank cursor
    CursorHandle := DllCall("CopyImage", "Ptr",  BlankCursor, "UInt", 2, "Int" ,  0, "Int",  0, "UInt", 0)
    DllCall("SetSystemCursor", "Ptr",  CursorHandle, "UInt", BusyCursor)
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
BigBox = %1%
HandlePSMC = %2%
PSMCPortable = %3%
PreScript = %4%
PostScript = %5%
PSMCOverride = %6%
HideTaskbar = %7%
MappedDrive = %8%

; Set Launchbox root directory
SplitPath, BigBox,, BaseDir

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
        BBRunFailed := 1
    }
    FileAppend, %A_Now% - INFO: Detected PSMC running at "%PSMCExe%". `n, LaunchBoxLauncher.log
}
else
{
    ; Using PSMC path override
    PSMCExe := PSMCOverride
    FileAppend, %A_Now% - INFO: Using override path for PSMC "%PSMCExe%". `n, LaunchBoxLauncher.log
}

; Check for License.xml
if FileExist(BaseDir "\License.xml")
{
    FileAppend, %A_Now% - INFO: File License.xml found in LaunchBox "%BaseDir%". `n, LaunchBoxLauncher.log
}
else
{
    FileAppend, %A_Now% - ERROR: File License.xml not found in LaunchBox "%BaseDir%". This script requires LaunchBox Premium to work. `n, LaunchBoxLauncher.log
    MsgBox, 0x10, Error, This script requires LaunchBox Premium in order to be able to launch BigBox., 5
    LicFailed := 1
}

; Check if License.xml check failed
if !LicFailed
{
    ;Hide Taskbar Ckeck
    if (HideTaskbar != "false")
    {
        FileAppend, %A_Now% - INFO: Hiding Taskbar. `n, LaunchBoxLauncher.log
        HideShowTaskbar(true)
    }

    ; Checks if LaunchBox.exe is running and kill it
    Process, Exist, LaunchBox.exe
    if ErrorLevel
    {
        FileAppend, %A_Now% - WARNING: Found LaunchBox.exe trying to close it now..., LaunchBoxLauncher.log
        Run, %comspec% /c taskkill /im Launchbox.exe,,Hide
        Run, %comspec% /c timeout /t 1 && tasklist /nh /fi "imagename eq Launchbox.exe" | find /i "Launchbox.exe" >nul && (taskkill /f /im Launchbox.exe),,Hide
        FileAppend, Killed. `n, LaunchBoxLauncher.log
        WinActivate, ahk_class PSMC
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
    WinGetPos, PSMCX, PSMCY,,, ahk_class PSMC
    Loop, %MonitorCount%
    {
        SysGet, Monitor, Monitor, %A_Index%
        if (MonitorLeft <= PSMCX and MonitorTop <= PSMCY and MonitorRight >= PSMCX and MonitorBottom >= PSMCY)
        {
            ScrHeight := MonitorBottom - MonitorTop
            ScrWidth := MonitorRight - MonitorLeft
            ScrX := MonitorLeft
            ScrY := MonitorTop
            FileAppend, %A_Now% - INFO: Monitor %A_Index% selected. `n, LaunchBoxLauncher.log
            break
        }
    }
}
else
{
    ScrHeight := A_ScreenHeight
    ScrWidth := A_ScreenWidth
    ScrX := 0
    ScrY := 0
}

; Load Blank GUI
FileAppend, %A_Now% - INFO: Loading blank gui at W%ScrWidth% H%ScrHeight% X%ScrX% Y%ScrY%. `n, LaunchBoxLauncher.log
Gui,Color,Black,000000
Gui, -Caption -dpiscale
Gui,Show, W%ScrWidth% H%ScrHeight% X%ScrX% Y%ScrY%

    ; Check if Bigbox.exe is already running
    FileAppend, %A_Now% - INFO: Starting all BigBox procedures. `n, LaunchBoxLauncher.log
    Process, Exist, %BigBox%
    if ErrorLevel
    {
        WinActivate, ahk_exe BigBox.exe
    }
    else
    {
        FileAppend, %A_Now% - INFO: Attempting to run "%BigBox%". `n, LaunchBoxLauncher.log
        Run, %BigBox%,,UseErrorLevel
        if ErrorLevel
        {
            FileAppend, %A_Now% - ERROR: %BigBox% failed to run. `n, LaunchBoxLauncher.log
            BBRunFailed := 1
        }
        else
        {
            FileAppend, %A_Now% - INFO: BigBox run successful. BigBox is starting up. `n, LaunchBoxLauncher.log
            ; Move Mouse to top right side of screen
            MouseMove, %A_ScreenWidth%, 0, 0

            ; Hide Mouse Cursor on gui
            DllCall("ShowCursor", "Int", 0)

            ; Hide Busy Cursor
            ShowBusy(False)

            ; Create group for Startup video support
            GroupAdd, BBStartup, VLC (Direct3D output) ahk_exe vlc.exe
            GroupAdd, BBStartup, ahk_exe BigBox.exe

            ; Wait for BigBox to run
            Process, Wait, BigBox.exe, 60
            if (ErrorLevel = 0)
            {
                FileAppend, %A_Now% - ERROR: Failed to detect BigBox in 60 seconds. Aborting. `n, LaunchBoxLauncher.log
                BBRunFailed := 1
            }
            else
            {
                FileAppend, %A_Now% - INFO: Process detected. BigBox.exe is running. `n, LaunchBoxLauncher.log
                ; Loading loop in case of error
                Loop
                {
                    Process, Exist, BigBox.exe
                    NewPID := ErrorLevel
                    if (NewPID = 0)
                    {
                        FileAppend, %A_Now% - ERROR: BigBox.exe is gone. Aborting. `n, LaunchBoxLauncher.log
                        BBRunFailed := 1
                        break
                    }
                    else
                    {
                        if WinExist("ahk_exe BigBox.exe")
                            break
                        else
                            continue
                    }
                    Sleep, 500
                }
            }
        }
    }
}
else
    BBRunFailed := 1

; Bigbox run error check
if !BBRunFailed
{
    PastFullFilename := ""
    ; Check if we need to minimise or close PSMC
    FileAppend, %A_Now% - INFO: Minimizing or exiting PSMC..., LaunchBoxLauncher.log
    if HandlePSMC
    {
        WinMinimize, ahk_class PSMC
    }
    else
    {
        Run, %comspec% /c taskkill /im PSMC.exe,,Hide
        Run, %comspec% /c timeout /t 1 && tasklist /nh /fi "imagename eq PSMC.exe" | find /i "PSMC.exe" >nul && (taskkill /f /im PSMC.exe),,Hide
    }
    FileAppend, Done. `n, LaunchBoxLauncher.log

    WinActivate, ahk_group BBStartup

    ; Main loop to monitor if Bigbox has been exited and if an update was found
    FileAppend, %A_Now% - INFO: Starting BigBox monitoring. `n, LaunchBoxLauncher.log
    Loop
    {
        ; Check if BigBox is behind blank window
        if WinActive("LaunchBoxLauncher-AHK.ahk") and WinExist("ahk_exe BigBox.exe")
            WinActivate, ahk_exe BigBox.exe

        ; Check if BigBox is closed
        if !WinExist("ahk_exe BigBox.exe")
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
                                    break
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
                                Process, WaitClose, BigBox.exe, 2
                                if ErrorLevel
                                {
                                    Run, %comspec% /c taskkill /im BigBox.exe,,Hide
                                    Run, %comspec% /c timeout /t 1 && tasklist /nh /fi "imagename eq BigBox.exe" | find /i "BigBox.exe" >nul && (taskkill /f /im BigBox.exe),,Hide
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
                                Process, Wait, BigBox.exe, 60
                                if (ErrorLevel = 0)
                                {
                                    FileAppend, %A_Now% - WARNING: Bigbox failed to relaunch within 60 seconds after installer closed. Update might have failed. `n, LaunchBoxLauncher.log
                                    SkipUpgrade := 1
                                    break
                                }
                                else
                                {
                                    WinActivate, ahk_exe BigBox.exe
                                    WinWaitNotActive, ahk_class SplashScreen
                                    WinWaitActive, ahk_exe BigBox.exe
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
    FileAppend, %A_Now% - INFO: BigBox monitoring completed. `n, LaunchBoxLauncher.log
}
FileAppend, %A_Now% - INFO: All BigBox procedures completed. `n, LaunchBoxLauncher.log

; Check for a Post-script
if (PostScript != "false" and !LicFailed)
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

; Bigbox run error check
if !BBRunFailed
{
    ; Check to see if PSMC is minimised or needs to be restarted
    FileAppend, %A_Now% - INFO: Maximizing or restarting PSMC..., LaunchBoxLauncher.log
    if HandlePSMC
    {
        WinMaximize, ahk_class PSMC
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

; Clean up to make sure BigBox is closed since we are now in PSMC again
FileAppend, %A_Now% - INFO: Making sure BigBox is now closed..., LaunchBoxLauncher.log
Process, Exist, BigBox.exe
if ErrorLevel
{
    Run, %comspec% /c taskkill /im BigBox.exe,,Hide
    Run, %comspec% /c timeout /t 1 && tasklist /nh /fi "imagename eq BigBox.exe" | find /i "BigBox.exe" >nul && (taskkill /f /im BigBox.exe),,Hide
}

FileAppend, Done. `n, LaunchBoxLauncher.log

; Restore Taskbar check
if (HideTaskbar != "false" and !LicFailed)
{
    FileAppend, %A_Now% - INFO: Restoring Taskbar. `n, LaunchBoxLauncher.log
    HideShowTaskbar(false)
}

; Restore Mouse Cursor
ShowBusy(True)

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