#!/usr/bin/env python3

#FIXME:
"""
    Copyright (C) ilias iliadis, 2018-12-21; ilias iliadis <>

    This file is part of Small Utils.

    Small Utils is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Small Utils is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Small Utils.  If not, see <http://www.gnu.org/licenses/>.
"""

#FIXME: correct the version
__version__ = '0.0.1'
VERSIONSTR = 'v. {}'.format(__version__)

#RETURN ERROR CODES
ERROR_IMPORT_LIBRARIES_FAIL = -1
ERROR_INVALID_GLADE_FILE = -2
ERROR_GLADE_FILE_READ = -3

try:
    import os
    import sys
    import subprocess

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk

    # Localization
    import locale
    from locale import gettext as _
    # Configuration and message boxes
    #from auxiliary import SectionConfig, OptionConfig
    #from auxiliary import MessageBox

except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

settings = None # Keep window related options
options = None #Keep application wide options in a 'General Options' section

def RemoveDS_Storefiles(thepath):
    cmnd = 'cd "' + thepath + '" && '
    cmnd += "find . -name '.DS_Store' -type f -delete"
    result = subprocess.Popen(cmnd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return result

def RemoveExecutableFromFiles(thepath):
    cmnd = 'cd "' + thepath + '" && '
    cmnd += "chmod -R -x+X *"
    result = subprocess.Popen(cmnd, shell=True, stdout=subprocess.PIPE).stdout.read()
    return result

class ChooserDialog:
    def __init__(self):
        #self.test = 0
        pass

    def select_folder(self, parentwindow):
        """ Select a Directory. """
        a = _("Please choose a directory")
        dialog = Gtk.FileChooserDialog('{}'.format(a,),
            parentwindow,
            Gtk.FileChooserAction.SELECT_FOLDER ,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))


        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return filename
        else:
            return None

