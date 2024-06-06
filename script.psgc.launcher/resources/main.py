# PSGC launcher by The Papaw. https://github.com/ThePapaw/psmc-19
# based on steam launcher by teeedubb. http://forum.xbmc.org/showthread.php?tid=157499
# Contribs: doogie
import os
import sys
import subprocess
import shutil
import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
from .lib.SMB import smb as smb

addon = xbmcaddon.Addon(id='script.psgc.launcher')
addonPath = addon.getAddonInfo('path')
addonIcon = addon.getAddonInfo('icon')
addonVersion = addon.getAddonInfo('version')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
scriptid = 'script.psgc.launcher'

launchbox = addon.getSetting("LaunchBox")
launchboxMode = addon.getSetting("LaunchBoxMode")
delUserScriptSett = addon.getSetting("DelUserScript")
showHideTaskbar = addon.getSetting("HideTaskbar")
quitPSMCSetting = addon.getSetting("QuitPSMC")
scriptUpdateCheck = addon.getSetting("ScriptUpdateCheck")
filePathCheck = addon.getSetting("FilePathCheck")
psmcPortable = addon.getSetting("PSMCPortable")
preScriptEnabled = addon.getSetting("PreScriptEnabled")
preScript = addon.getSetting("PreScript")
postScriptEnabled = addon.getSetting("PostScriptEnabled")
postScript = addon.getSetting("PostScript")
osWin = xbmc.getCondVisibility('system.platform.windows')
suspendAudio = addon.getSetting("SuspendAudio")
uwaScriptLocEnabled = addon.getSetting("UWAScriptLocEnabled")
uwaScriptLoc = addon.getSetting("UWAScriptLoc")
overridePSMCLocEnabled = addon.getSetting("OverridePSMCLocEnabled")
overridePSMCLoc = addon.getSetting("OverridePSMCLoc")
autohotkeyExe = addon.getSetting("AutohotkeyLoc")
overrideAHK = addon.getSetting("AutohotkeyLocEnabled")
psmcPath = "false"
smbDrive = "0"


def log(msg):
    xbmc.log('%s: %s' % (scriptid, msg))


def getAddonInstallPath():
    path = addon.getAddonInfo('path')
    return path


def getAddonDataPath():
    if uwaScriptLocEnabled == 'true':
        if not uwaScriptLoc == '':
            path = uwaScriptLoc
        else:
            log('ERROR: UWA save location not set in settings')
            dialog.notification(language(50123), language(50129), addonIcon, 5000)
            sys.exit()
    else:
        path = xbmcvfs.translatePath('special://profile/addon_data/%s' % scriptid)
        if not os.path.exists(path):
            log('addon userdata folder does not exist, creating: %s' % path)
            try:
                os.makedirs(path)
                log('created directory: %s' % path)
            except OSError:
                log('ERROR: failed to create directory: %s' % path)
                dialog.notification(language(50123), language(50126), addonIcon, 5000)
    return path


def copyLauncherScriptsToUserdata():
    oldBasePath = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
    newBasePath = os.path.join(getAddonDataPath(), 'scripts')

    oldPath = os.path.join(oldBasePath, 'LaunchboxLauncher-AHK.ahk')
    newPath = os.path.join(newBasePath, 'LaunchBoxLauncher-AHK.ahk')
    copyFile(oldPath, newPath)
    oldPath = os.path.join(oldBasePath, 'BigBoxLauncher-AHK.ahk')
    newPath = os.path.join(newBasePath, 'BigBoxLauncher-AHK.ahk')
    copyFile(oldPath, newPath)
    oldPath = os.path.join(oldBasePath, 'LaunchBoxLauncher-AHK.ico')
    newPath = os.path.join(newBasePath, 'LaunchBoxLauncher-AHK.ico')
    copyFile(oldPath, newPath)


def copyAutoHotkeyToUserdata():
    global autohotkeyExe
    newBasePath = os.path.join(getAddonDataPath(), 'AutoHotkey')
    oldPath = autohotkeyExe
    newAutohotkeyPath = os.path.join(newBasePath, 'AutoHotkey.exe')
    if overrideAHK == 'false' and oldPath != newAutohotkeyPath or not os.path.isfile(oldPath):
        autohotkeyPath = locateAutoHotkey()
        log('trying to copy AutoHotkey to userdata folder')
        oldPath = os.path.join(autohotkeyPath, 'AutoHotkey.exe')
        copyFile(oldPath, newAutohotkeyPath)
        oldPath = os.path.join(autohotkeyPath, 'license.txt')
        newPath = os.path.join(newBasePath, 'license.txt')
        if os.path.isfile(oldPath):
            copyFile(oldPath, newPath)
        autohotkeyExe = newAutohotkeyPath
        log('updating AutoHotkey location setting to: %s' % newAutohotkeyPath)
        addon.setSetting(id="AutohotkeyLoc", value=newAutohotkeyPath)
    elif overrideAHK == 'true':
        log('using user selected AutoHotkey location: %s' % autohotkeyExe)
    else:
        log('using AutoHotkey location: %s' % autohotkeyExe)


def copyFile(oldPath, newPath):
    newDir = os.path.dirname(newPath)
    if not os.path.isdir(newDir):
        log('required userdata folder does not exist, creating: %s' % newDir)
        try:
            os.mkdir(newDir)
            log('sucsessfully created userdata folder: %s' % newDir)
        except OSError:
            log('ERROR: failed to create userdata folder: %s' % newDir)
            dialog.notification(language(50123), language(50126), addonIcon, 5000)
            sys.exit()
    if not os.path.isfile(newPath):
        log('file does not exist, copying to userdata: %s' % newPath)
        try:
            shutil.copy2(oldPath, newPath)
            log('sucsessfully copied userdata file: %s' % newPath)
        except OSError:
            log('ERROR: failed to copy file to userdata: %s' % newPath)
            dialog.notification(language(50123), language(50126), addonIcon, 5000)
            sys.exit()
    else:
        log('file already exists, skipping copy to userdata: %s' % newPath)


def usrScriptDelete():
    if delUserScriptSett == 'true':
        log('deleting userdata scripts, option enabled: delUserScriptSett = %s' % delUserScriptSett)
        scriptFile = os.path.join(getAddonDataPath(), 'scripts', 'LaunchBoxLauncher-AHK.ahk')
        delUserScript(scriptFile)
        scriptFile = os.path.join(getAddonDataPath(), 'scripts', 'BigBoxLauncher-AHK.ahk')
        delUserScript(scriptFile)
        scriptFile = os.path.join(getAddonDataPath(), 'scripts', 'LaunchBoxLauncher-AHK.ico')
        delUserScript(scriptFile)
        scriptFile = os.path.join(getAddonDataPath(), 'AutoHotkey', 'AutoHotkey.exe')
        delUserScript(scriptFile)
        scriptFile = os.path.join(getAddonDataPath(), 'AutoHotkey', 'license.txt')
        delUserScript(scriptFile)
        addon.setSetting(id="DelUserScript", value="false")
    elif delUserScriptSett == 'false':
        log('skipping deleting userdata scripts, option disabled: delUserScriptSett = %s' % delUserScriptSett)


def delUserScript(scriptFile):
    if os.path.isfile(scriptFile):
        try:
            os.remove(scriptFile)
            log('found and deleting: %s' % scriptFile)
        except OSError:
            log('ERROR: deleting failed: %s' % scriptFile)
            dialog.notification(language(50123), language(50126), addonIcon, 5000)


def findAppPath(program):
    result = ''
    ignore_dirs = {'Backups', 'Data', 'Games', 'Images', 'LBThemes', 'Logs', 'Manuals', 'Metadata', 'Music',
                   'PauseThemes', 'Sounds', 'StartupThemes', 'Themes', 'Updates', 'Videos'}
    for root, dirs, files in os.walk(launchbox):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        files[:] = [f for f in files if f.endswith('.exe')]
        if program in files:
            result = root
    return result


def locateAutoHotkey():
    log('attempting to locate Autohotkey')
    autohotkeyExePath = findAppPath('AutoHotkey.exe')
    if autohotkeyExePath == '':
        dialog.notification(language(50123), language(50136), addonIcon, 5000)
        log('ERROR: AutoHotkey.exe not found')
        mappedDrive('destroy')
        sys.exit()
    else:
        log('AutoHotkey path found: %s' % autohotkeyExePath)
    return autohotkeyExePath


def fileChecker():
    if filePathCheck == 'true':
        log('running program file check, option is enabled: filePathCheck = %s' % filePathCheck)
        launchboxExe = os.path.join(launchbox, '%s.exe' % ("BigBox" if launchboxMode == '0' else "LaunchBox"))
        programFileCheck(launchboxExe)
    else:
        log('skipping program file check, option disabled: filePathCheck = %s' % filePathCheck)


def fileCheckDialog(programExe):
    log('ERROR: dialog to go to addon settings because executable does not exist: %s' % programExe)
    if dialog.yesno(language(50123), '%s\n%s\n%s' % (programExe, language(50122), language(50121))):
        log('yes selected, opening addon settings')
        mappedDrive('destroy')
        addon.openSettings()
        mappedDrive('create')
        fileChecker()
        mappedDrive('destroy')
        sys.exit()
    else:
        log('ERROR: no selected with invalid executable, exiting: %s' % programExe)
        mappedDrive('destroy')
        sys.exit()


def programFileCheck(launchboxExe):
    if os.path.isfile(os.path.join(launchboxExe)):
        log('Program executable exists %s' % launchboxExe)
    else:
        fileCheckDialog(launchboxExe)


def scriptVersionCheck():
    if scriptUpdateCheck == 'true':
        log('usr scripts are set to be checked for updates...')
        if delUserScriptSett == 'false':
            log('usr scripts are not set to be deleted, running version check')
            sysScriptDir = os.path.join(getAddonInstallPath(), 'resources', 'scripts')
            usrScriptDir = os.path.join(getAddonDataPath(), 'scripts')
            sysScriptPath = os.path.join(sysScriptDir, '%sLauncher-AHK.ahk' % ("BigBox" if launchboxMode == '0' else "LaunchBox"))
            usrScriptPath = os.path.join(usrScriptDir, '%sLauncher-AHK.ahk' % ("BigBox" if launchboxMode == '0' else "LaunchBox"))
            if os.path.isfile(os.path.join(usrScriptPath)):
                compareFile(sysScriptPath, usrScriptPath)
            else:
                log('usr script does not exist, skipping version check')
        else:
            log('usr scripts are set to be deleted, no version check needed')
    else:
        log('usr scripts are set to not be checked for updates, skipping version check')


def compareFile(sysScriptPath, usrScriptPath):
    global delUserScriptSett
    scriptSysVer = '000'
    scriptUsrVer = '000'
    if os.path.isfile(sysScriptPath):
        with open(sysScriptPath, 'r') as f:
            for line in f.readlines():
                if "llsrevision=" in line:
                    scriptSysVer = line[12:15]
        log('sys "llsrevision=": %s' % scriptSysVer)
    if os.path.isfile(usrScriptPath):
        with open(usrScriptPath, 'r') as f:
            for line in f.readlines():
                if "llsrevision=" in line:
                    scriptUsrVer = line[12:15]
        log('usr "llsrevision=": %s' % scriptUsrVer)
    if scriptSysVer > scriptUsrVer:
        log('system scripts have been updated: sys:%s > usr:%s' % (scriptSysVer, scriptUsrVer))
        if dialog.yesno(language(50113), '%s\n%s' % (language(50124), language(50125))):
            delUserScriptSett = 'true'
            log('yes selected, option delUserScriptSett enabled: %s' % delUserScriptSett)
        else:
            delUserScriptSett = 'false'
            log('no selected, script update check disabled: ScriptUpdateCheck = %s' % scriptUpdateCheck)
    else:
        log('userdata script are up to date')


def mappedDrive(task):
    global smbDrive
    global launchbox
    if task == 'create':
        smbDrive, launchbox = smb.createMappedDrive(launchbox)
    if task == 'destroy':
        smbDrive = smb.destroyMappedDrive(smbDrive)


def quitPSMCDialog():
    global quitPSMCSetting
    if quitPSMCSetting == '2':
        log('quit setting: %s selected, asking user to pick' % quitPSMCSetting)
        if dialog.yesno('LaunchBox Launcher', language(50073)):
            quitPSMCSetting = '0'
        else:
            quitPSMCSetting = '1'
    log('quit setting selected: %s' % quitPSMCSetting)


def launchboxPrePost():
    global postScript
    global preScript
    if preScriptEnabled == 'false':
        preScript = 'false'
    elif preScriptEnabled == 'true':
        if not os.path.isfile(os.path.join(preScript)):
            log('pre-launchbox script does not exist, disabling!: "%s"' % preScript)
            preScript = 'false'
            dialog.notification(language(50123), language(50126), addonIcon, 5000)
    elif preScript == '':
        preScript = 'false'
    log('pre launchbox script: %s' % preScript)
    if postScriptEnabled == 'false':
        postScript = 'false'
    elif preScriptEnabled == 'true':
        if not os.path.isfile(os.path.join(postScript)):
            log('post-launchbox script does not exist, disabling!: "%s"' % postScript)
            postScript = 'false'
            dialog.notification(language(50123), language(50126), addonIcon, 5000)
    elif postScript == '':
        postScript = 'false'
    log('post launchbox script: %s' % postScript)


def psmcOverrideDetect():
    global psmcPath
    if overridePSMCLocEnabled == 'true':
        if not overridePSMCLoc == '':
            if not os.path.isfile(os.path.join(overridePSMCLoc)):
                log('PSMC.exe does not exist.')
                dialog.notification(language(50123), language(50133), addonIcon, 5000)
                sys.exit()
            psmcPath = overridePSMCLoc
        else:
            log('ERROR: PSMC Override location not set in settings')
            dialog.notification(language(50123), language(50132), addonIcon, 5000)
            sys.exit()
    else:
        psmcPath = 'false'


def launchLaunchBox():
    basePath = os.path.join(getAddonDataPath(), 'scripts')
    modeExe = os.path.join(launchbox, '%s.exe' % ("BigBox" if launchboxMode == '0' else "LaunchBox"))
    if autohotkeyExe == '':
        dialog.notification(language(50123), language(50136), addonIcon, 5000)
        log('ERROR: AutoHotkey.exe not found')
        sys.exit()
    launchboxLauncher = os.path.join(basePath, '%sLauncher-AHK.ahk' % ("BigBox" if launchboxMode == '0' else "LaunchBox"))
    cmd = '"%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (
                autohotkeyExe, launchboxLauncher, modeExe, quitPSMCSetting, psmcPortable,
                preScript, postScript, psmcPath, showHideTaskbar, smbDrive)
    try:
        log('attempting to launch: %s' % cmd)
        if quitPSMCSetting == '1':
            if suspendAudio == 'true':
                xbmc.audioSuspend()
                log('Audio suspended')
            proc_h = subprocess.Popen(cmd, shell=True, close_fds=False)
            log('Idle Shutdown timer disabled')
            xbmc.executebuiltin("InhibitIdleShutdown(True)")
            log('Waiting for LaunchBox to exit')
            while proc_h.returncode is None:
                xbmc.sleep(1000)
                proc_h.poll()
            del proc_h
            log('Idle Shutdown timer enabled')
            xbmc.executebuiltin("InhibitIdleShutdown(False)")
            if suspendAudio == 'true':
                log('Start resuming audio....')
                xbmc.audioResume()
                log('Audio resumed')
        else:
            subprocess.Popen(cmd, shell=True, close_fds=True)
    except OSError:
        log('ERROR: failed to launch: %s' % cmd)
        dialog.notification(language(50123), language(50126), addonIcon, 5000)
        mappedDrive('destroy')


def launchboxMain():
    scriptVersionCheck()
    usrScriptDelete()
    copyLauncherScriptsToUserdata()
    psmcOverrideDetect()
    mappedDrive('create')
    fileChecker()
    copyAutoHotkeyToUserdata()
    launchboxPrePost()
    quitPSMCDialog()
    launchLaunchBox()


log('****Running LaunchBox-Launcher v%s....' % addonVersion)
launchboxMain()
