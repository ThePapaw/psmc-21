import re
import sys
import subprocess
import xbmc
import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon(id='script.psgc.launcher')
addonIcon = addon.getAddonInfo('icon')
dialog = xbmcgui.Dialog()
language = addon.getLocalizedString
scriptid = 'script.psgc.launcher'


def log(msg):
    xbmc.log('%s: %s' % (scriptid, msg))


def IPCheckDialog():
    log('ERROR: dialog to go to addon settings because smb over ip was used:')
    if dialog.yesno(language(50123), language(50135), language(50121)):
        log('yes selected, opening addon settings')
        addon.openSettings()
        sys.exit()
    else:
        log('ERROR: no selected, cannot use ip, exiting')
        sys.exit()


def createMappedDrive(launchboxCheck):
    overrideSmbIPEnabled = addon.getSetting("OverrideSmbIPEnabled")
    overrideSmbIP = addon.getSetting("OverrideSmbIP")
    smbDrive = "0"

    if launchboxCheck[0:3] == 'smb':
        log('smb detected, creating mapped network drive')
        smbConn = re.split('[:@]', launchboxCheck[6:])

        if len(smbConn) == 3:
            smbUser = smbConn[0]
            smbPass = smbConn[1]
            smbArr = re.split('/', smbConn[2])
            if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', smbArr[0]):
                log('IP detected: smb mapping over ip not supported due to windows security')
                if overrideSmbIPEnabled == 'true':
                    smbArr[0] = overrideSmbIP
                    log('Using IP override, Hostname: %s' % overrideSmbIP)
                else:
                    IPCheckDialog()
            smbAddr = '\\\\' + "\\".join(smbArr)
            if smbAddr[:-1] == "\\":
                smbAddr = smbAddr[-1:]
            smbAddr = smbAddr[:-(len(smbArr[-2])) - 1]
            smbCmd = "net use * " + smbAddr[:-1] + " /user:" + smbUser + " " + smbPass
        else:
            smbArr = re.split('/', smbConn[0])
            if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', smbArr[0]):
                log('IP detected: smb mapping over ip not supported due to windows security')
                if overrideSmbIPEnabled == 'true':
                    log('Using IP override, Hostname: %s' % overrideSmbIP)
                    smbArr[0] = overrideSmbIP
                else:
                    IPCheckDialog()
            smbAddr = '\\\\' + "\\".join(smbArr)
            if smbAddr[-1:] == "\\":
                smbAddr = smbAddr[:-1]
            smbAddr = smbAddr[:-(len(smbArr[-2])) - 1]
            smbCmd = "net use * " + smbAddr

        p = subprocess.Popen(smbCmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        if p_status == 0:
            smbDrive = output[6:8].decode()
            launchbox = smbDrive + '\\' + smbArr[-2] + '\\'
            return smbDrive, launchbox
        else:
            log('error on mapped drive creation: %s' % p_status)
            dialog.notification(language(50123), language(50134), addonIcon, 5000)
            sys.exit()
    else:
        log('not a smb share skipping mapped drive creation')
        return smbDrive, launchboxCheck


def destroyMappedDrive(smbDrive):
    if smbDrive != "0":
        log('attempting to remove mapped drive')
        smbCmd = "net use " + smbDrive + " /delete /y"
        p = subprocess.Popen(smbCmd, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()

        if p_status == 0:
            smbDrive = "0"
            log('mapped drive successfully deleted')
            return smbDrive
        else:
            log('error on mapped drive deletion: %s' % p_status)
            sys.exit()
    else:
        log('no mapped drive was created so nothing to clean up')

