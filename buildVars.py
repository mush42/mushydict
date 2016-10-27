# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/src/56140dbec531e4d7591338e1dbc6192f3dd422a8/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "mushydict",
	# Add-on summary, usually the user visible name of the addon.
	# TRANSLATORS: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Mushy Dictionary"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""
    A Little Arabic - English, English - Arabic dictionary for your NVDA.
    Select a phrase and then press NVDA plus D to show translations.    
    """),
	# version
	"addon_version" : "1.0",
	# Author(s)
	"addon_author" : "Musharraf Omer <ibnomer2011@hotmail.com>",
	# URL for the add-on documentation support
	"addon_url" : "",
	# File name for the add-on help file.
	"addon_docFileName" : "readme.html"
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [os.path.join('addon', 'globalPlugins', 'mushydict', filename) for filename in ('__init__.py', 'dialogs.py', 'deps')]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
