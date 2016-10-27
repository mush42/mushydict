r"""
* A Little Arabic - English, English - Arabic Dictionary for your NVDA.
* Crafted by Musharraf Omer <ibnomer2011@hotmail.com>.
* The dictionary data is from <https://github.com/devjustly/en_ar_dict>.
* Licensed under the GNU General Public License.
""" 

import os
import re
import wx

import globalPluginHandler
import gui
import api
import textInfos
import ui

from .deps import sqlite3
from .dialogs import ResultsDialog

ADDON_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(ADDON_DIR, 'dictdata', 'data.db')
latin = re.compile(r'^[a-zA-Z]') # if it starts with a latin letter, we assume it is an English word

# Enable i18n.
import addonHandler
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super(globalPluginHandler.GlobalPlugin, self).__init__()
        con = sqlite3.connect(DB_PATH)
        self.cursor = con.cursor()

    def script_translate_phrase(self, gesture):
        phrase = self.getSelectedText()
        if not phrase:
            return ui.message(_("No selection"))
        gui.mainFrame._popupSettingsDialog(ResultsDialog, data=self.translate(phrase))
    script_translate_phrase.__doc__ = _("Translates selected phrase using Mushy Dictionary")

    def getSelectedText(self):
        obj=api.getFocusObject()
        treeInterceptor=obj.treeInterceptor
        if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
            obj=treeInterceptor
        try:
            info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
        except (RuntimeError, NotImplementedError):
            info=None
        if not info or info.isCollapsed:
            return None
        return info.clipboardText

    def translate(self, word):
        eng = latin.match(word)
        if eng is not None:
            sql = "select * from words_list where en like '%%%s%%' limit 10" %word
        else:
            sql = "select * from words_list where ar like '%%%s%%' limit 10" %word
        return ((i[2], i[3]) if eng else (i[3], i[2]) for i in self.cursor.execute(sql).fetchall())

    __gestures = {'kb:nvda+d': 'translate_phrase'}