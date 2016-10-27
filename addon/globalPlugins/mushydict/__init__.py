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
        lang = 'en' if latin.match(word) else 'ar'
        probable = "select * from words_list where %s like '%s' limit 5" %(lang, word)
        probable_2 = "select * from words_list where %s like '%s%%' limit 8" %(lang, word)
        any = "select * from words_list where %s like '%%%s%%' limit 5" %(lang, word)
        rv = list(self.cursor.execute(probable).fetchall())
        rv.extend([item for item in self.cursor.execute(probable_2).fetchall() if item not in rv])
        rv.extend([item for item in self.cursor.execute(any).fetchall() if item not in rv])
        return ((i[2], i[3]) if lang=='en' else (i[3], i[2]) for i in rv)

    __gestures = {'kb:nvda+d': 'translate_phrase'}