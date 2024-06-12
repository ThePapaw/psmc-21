"""
	FuzzyBritches Add-on (Yay for new custom dialogs. thanks Peter for the help)
"""
from resources.lib.modules.control import addonIcon, getLangString as getLS, setting as getSetting, darkColor
from resources.lib.windows.base import BaseDialog

class OK(BaseDialog):
    def __init__(self, *args, **kwargs):
        BaseDialog.__init__(self, args)
        self.ok_label = kwargs.get('ok_label')
        self.text =  kwargs.get('text')
        self.heading = kwargs.get('heading', getLS(40414))
        self.icon = kwargs.get('icon', addonIcon())
        self.lightordark = getSetting('dialogs.lightordarkmode')
        self.buttonColor = getSetting('dialogs.button.color')
        self.customBackgroundColor = getSetting('dialogs.customcolor', 'FF000000')
        self.dark_text_background = darkColor(self.customBackgroundColor)
        self.useCustomTitleColor = getSetting('dialogs.usecolortitle') == 'true'
        self.customTitleColor = getSetting('dialogs.titlebar.color')
        self.set_properties()

    def run(self):
        self.doModal()

    def onClick(self, controlID):
        self.close()

    def onAction(self, action):
        if action in self.closing_actions:
            self.doClose()

    def doClose(self):
        self.close()
        del self
        

    def set_properties(self):
        self.setProperty('ok_label', self.ok_label)
        self.setProperty('text', self.text)
        self.setProperty('heading', self.heading)
        self.setProperty('fuzzybritches.buttonColor', self.buttonColor)
        if self.useCustomTitleColor:
            #need to use a custom titlebar color
            self.setProperty('fuzzybritches.titleBarColor', self.customTitleColor)
            if darkColor(self.customTitleColor) == 'dark':
                self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
            else:
                self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
        if darkColor(self.buttonColor) == 'dark':
            self.setProperty('fuzzybritches.buttonTextColor', 'FFF5F5F5')
        else:
            self.setProperty('fuzzybritches.buttonTextColor', 'FF302F2F')
        if self.lightordark == '0':
            self.setProperty('fuzzybritches.backgroundColor', 'FF302F2F') #setting dark grey for dark mode
            self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
            self.setProperty('fuzzybritches.buttonnofocus', '33F5F5F5')
            if not self.useCustomTitleColor:
                self.setProperty('fuzzybritches.titleBarColor', 'FF302F2F')
                self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
            self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
        elif self.lightordark == '1':
            self.setProperty('fuzzybritches.backgroundColor', 'FFF5F5F5') #setting dirty white for light mode. (the hell you call me)
            self.setProperty('fuzzybritches.textColor', 'FF302F2F')
            self.setProperty('fuzzybritches.buttonnofocus', '33302F2F')
            if not self.useCustomTitleColor:
                self.setProperty('fuzzybritches.titleBarColor', 'FFF5F5F5')
                self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
            self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
        elif self.lightordark == '2':
            #ohh now we need a custom color, aren't we just special.
            self.setProperty('fuzzybritches.backgroundColor', self.customBackgroundColor) #setting custom color because screw your light or dark mode.
            if self.dark_text_background == 'dark':
                self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
                self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
                self.setProperty('fuzzybritches.buttonnofocus', 'FFF5F5F5')
                if not self.useCustomTitleColor:
                    self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
                    self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor) #setting titletext and background color if not using a custom value
            else:
                self.setProperty('fuzzybritches.textColor', 'FF302F2F')
                self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
                self.setProperty('fuzzybritches.buttonnofocus', '33302F2F')
                if not self.useCustomTitleColor:
                    self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
                    self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor)#setting titletext and background color if not using a custom value

class Confirm(BaseDialog):
    def __init__(self, *args, **kwargs):
        BaseDialog.__init__(self, args)
        self.ok_label = kwargs.get('ok_label')
        self.cancel_label = kwargs.get('cancel_label')
        self.text =  kwargs.get('text')
        self.heading = kwargs.get('heading', getLS(40414))
        self.icon = kwargs.get('icon', addonIcon())
        self.default_control = kwargs.get('default_control')
        self.lightordark = getSetting('dialogs.lightordarkmode')
        self.buttonColor = getSetting('dialogs.button.color')
        self.customBackgroundColor = getSetting('dialogs.customcolor')
        self.customBackgroundColor = getSetting('dialogs.customcolor', 'FF000000')
        self.useCustomTitleColor = getSetting('dialogs.usecolortitle') == 'true'
        self.customTitleColor =getSetting('dialogs.titlebar.color')
        self.selected = None
        self.set_properties()


    def onInit(self):
        self.set_properties()
        self.setFocusId(self.default_control)

    def run(self):
        self.doModal()
        return self.selected

    def onClick(self, controlID):
        if controlID == 10: self.selected = True
        elif controlID == 11: self.selected = False
        self.close()

    def onAction(self, action):
        if action in self.closing_actions: self.close()

    def set_properties(self):
        self.setProperty('ok_label', self.ok_label)
        self.setProperty('cancel_label', self.cancel_label)
        self.setProperty('text', self.text)
        self.setProperty('heading', self.heading)
        self.setProperty('fuzzybritches.buttonColor', self.buttonColor)
        if self.useCustomTitleColor:
            #need to use a custom titlebar color
            self.setProperty('fuzzybritches.titleBarColor', self.customTitleColor)
            if darkColor(self.customTitleColor) == 'dark':
                self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
            else:
                self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
        if darkColor(self.buttonColor) == 'dark':
            self.setProperty('fuzzybritches.buttonTextColor', 'FFF5F5F5')
        else:
            self.setProperty('fuzzybritches.buttonTextColor', 'FF302F2F')
        if self.lightordark == '0':
            self.setProperty('fuzzybritches.backgroundColor', 'FF302F2F') #setting dark grey for dark mode
            self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
            self.setProperty('fuzzybritches.buttonnofocus', '33F5F5F5')
            if not self.useCustomTitleColor:
                self.setProperty('fuzzybritches.titleBarColor', 'FF302F2F')
                self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
            self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
        elif self.lightordark == '1':
            self.setProperty('fuzzybritches.backgroundColor', 'FFF5F5F5') #setting dirty white for light mode. (the hell you call me)
            self.setProperty('fuzzybritches.textColor', 'FF302F2F')
            self.setProperty('fuzzybritches.buttonnofocus', '33302F2F')
            if not self.useCustomTitleColor:
                self.setProperty('fuzzybritches.titleBarColor', 'FFF5F5F5')
                self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
            self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
        elif self.lightordark == '2':
            #ohh now we need a custom color, aren't we just special.
            self.setProperty('fuzzybritches.backgroundColor', self.customBackgroundColor) #setting custom color because screw your light or dark mode.
            if self.dark_text_background == 'dark':
                self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
                self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
                self.setProperty('fuzzybritches.buttonnofocus', 'FFF5F5F5')
                if not self.useCustomTitleColor:
                    self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
                    self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor) #setting titletext and background color if not using a custom value
            else:
                self.setProperty('fuzzybritches.textColor', 'FF302F2F')
                self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
                self.setProperty('fuzzybritches.buttonnofocus', '33302F2F')
                if not self.useCustomTitleColor:
                    self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
                    self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor)#setting titletext and background color if not using a custom value

class ProgressFuzzyBritches(BaseDialog):
    def __init__(self, *args, **kwargs):
        BaseDialog.__init__(self, args)
        self.window_id = 2095
        self.closed = False
        self.icon = kwargs.get('icon', addonIcon())
        self.heading = kwargs.get('heading', getLS(40414))
        self.qr = kwargs.get('qr')
        self.artwork = kwargs.get('artwork')
        self.lightordark = getSetting('dialogs.lightordarkmode')
        self.buttonColor = getSetting('dialogs.button.color')
        self.customBackgroundColor = getSetting('dialogs.customcolor', 'FF000000')
        self.dark_text_background = darkColor(self.customBackgroundColor)
        self.useCustomTitleColor = getSetting('dialogs.usecolortitle') == 'true'
        self.customTitleColor = getSetting('dialogs.titlebar.color')

    def run(self):
        self.doModal()
        self.clearProperties()

    def onAction(self, action):
        if action in self.closing_actions or action in self.selection_actions:
            self.doClose()

    def doClose(self):
        self.closed = True
        self.close()
        del self

    def iscanceled(self):
        return self.closed

    def set_controls(self):
        if self.qr == 1:
            self.getControl(200).setImage(self.icon)
            self.setProperty('fuzzybritches.qr','1')
        else:
            self.setProperty('fuzzybritches.qr','0')
        if self.artwork == 1:
            self.setProperty('fuzzybritches.qr','0')
            self.setProperty('fuzzybritches.artwork', '1')
            self.getControl(201).setImage(self.icon)
        else:
            self.setProperty('fuzzybritches.artwork', '0')
        self.setProperty('fuzzybritches.buttonColor', self.buttonColor)
        if self.useCustomTitleColor:
            #need to use a custom titlebar color
            self.setProperty('fuzzybritches.titleBarColor', self.customTitleColor)
            if darkColor(self.customTitleColor) == 'dark':
                self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
            else:
                self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
        if darkColor(self.buttonColor) == 'dark':
            self.setProperty('fuzzybritches.buttonTextColor', 'FFF5F5F5')
        else:
            self.setProperty('fuzzybritches.buttonTextColor', 'FF302F2F')
        if self.lightordark == '0':
            self.setProperty('fuzzybritches.backgroundColor', 'FF302F2F') #setting dark grey for dark mode
            self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
            self.setProperty('fuzzybritches.buttonnofocus', '33F5F5F5')
            if not self.useCustomTitleColor:
                self.setProperty('fuzzybritches.titleBarColor', 'FF302F2F')
                self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
            self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
        elif self.lightordark == '1':
            self.setProperty('fuzzybritches.backgroundColor', 'FFF5F5F5') #setting dirty white for light mode. (the hell you call me)
            self.setProperty('fuzzybritches.textColor', 'FF302F2F')
            self.setProperty('fuzzybritches.buttonnofocus', '33302F2F')
            if not self.useCustomTitleColor:
                self.setProperty('fuzzybritches.titleBarColor', 'FFF5F5F5')
                self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
            self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
        elif self.lightordark == '2':
            #ohh now we need a custom color, aren't we just special.
            self.setProperty('fuzzybritches.backgroundColor', self.customBackgroundColor) #setting custom color because screw your light or dark mode.
            if self.dark_text_background == 'dark':
                self.setProperty('fuzzybritches.textColor', 'FFF5F5F5')
                self.setProperty('fuzzybritches.buttonTextColorNS', 'FFF5F5F5')
                self.setProperty('fuzzybritches.buttonnofocus', 'FFF5F5F5')
                if not self.useCustomTitleColor:
                    self.setProperty('fuzzybritches.titleTextColor', 'FFF5F5F5')
                    self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor) #setting titletext and background color if not using a custom value
            else:
                self.setProperty('fuzzybritches.textColor', 'FF302F2F')
                self.setProperty('fuzzybritches.buttonTextColorNS', 'FF302F2F')
                self.setProperty('fuzzybritches.buttonnofocus', '33302F2F')
                if not self.useCustomTitleColor:
                    self.setProperty('fuzzybritches.titleTextColor', 'FF302F2F')
                    self.setProperty('fuzzybritches.titleBarColor', self.customBackgroundColor)#setting titletext and background color if not using a custom value

    def update(self, percent=0, content='', icon=None):
        try:
            self.setProperty('fuzzybritches.label', self.heading)
            self.setProperty('percent', str(percent))
            self.getControl(2001).setText(content)
            self.getControl(5000).setPercent(percent)
            if icon:
                if self.artwork == '1':
                    self.getControl(201).setImage(icon)
                else:
                    self.geControl(200).setImage(icon)
        except: pass