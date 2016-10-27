# -*- coding: utf-8 -*-

# Copyright (c) 2016 Musharraf Omer
# This file is covered by the GNU General Public License.

import wx
import gui

# Enable i18n.
import addonHandler
addonHandler.initTranslation()

class ResultsDialog(gui.SettingsDialog):
    title = _("Mushy Dictionary")
    
    def __init__(self, parent, *args, **kwargs):
        self.data = kwargs.pop('data', [])
        super(ResultsDialog, self).__init__(parent, *args, **kwargs)

    def makeSettings(self, settingsSizer):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        listLabel = wx.StaticText(self,-1, label=_("&Matches"))
        self.translationList = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL, size=(550, 350))
        self.translationList.InsertColumn(0, _("Phrase"), width=150)
        self.translationList.InsertColumn(1,_("Translation"), width=150)
        mainSizer.Add(listLabel)
        mainSizer.Add(self.translationList)
        settingsSizer.Add(mainSizer,border=10,flag=wx.BOTTOM)
        
    def postInit(self):
        for trans in self.data:
            self.translationList.Append(trans)
        self.translationList.SetFocus()
