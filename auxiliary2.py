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

CUSTOM_KEYS_PARENT_SCHEMA = "org.cinnamon.desktop.keybindings"
CUSTOM_KEYS_BASENAME = "/org/cinnamon/desktop/keybindings/custom-keybindings"
CUSTOM_KEYS_SCHEMA = "org.cinnamon.desktop.keybindings.custom-keybinding"

DEFAULT_KEY_COMBINATION = '<Primary><Shift>F12'

try:
    import os
    import sys
    import subprocess
    import re

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk

    #gi.require_version('Notify', '0.7')
    #from gi.repository import Notify
    from gi.repository import Gio

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

BARE_SYNAPTICS_BASH_TEXT = """#!/bin/bash
# Get the device id of the Synaptics TouchPad
id=$(xinput list --id-only '{}')

# Get the current state of the Device Enabled property
# The devString will look like: "Device Enabled (132): 0"
devString=$(xinput --list-props $id | grep "Device Enabled")

# Parse the devString into an array
read -a devString_array <<< "$devString"

# Save the current state of the Device Enabled property
# from the 4th element of devString_array
devEnabled=${{devString_array[3]}}

# Flip the state of the Device Enabled property
if [ $devEnabled -eq 1 ]; then
    devEnabled=0
else
    devEnabled=1
fi

# Set the "Device Enabled" property with the new value
xinput set-prop $id "Device Enabled" $devEnabled

# Push out a desktop notification of the new value
notify-send --icon computer "Synaptics TouchPad" "Device Enabled = $devEnabled"
exit
"""

get_output = lambda cmd: subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")

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

def create_synaptics_bash_file(synapticsname):
    cmd = BARE_SYNAPTICS_BASH_TEXT.format(synapticsname,)
    return cmd

def extract_key_combinations_from_string(astring):
    pattern = "<.+?>"
    all_keys = re.findall(pattern, astring, flags=0)
    specialkeys = []
    simplekey = ''

    for aspecialkey in all_keys:
        specialkeys.append(aspecialkey[1:-1])
        astring = astring.replace(aspecialkey, "")
    simplekey = astring.strip()
    return specialkeys, simplekey


def get_shorcut_combinations(my_combination=DEFAULT_KEY_COMBINATION):

    key_combinations_bundled = []
    key_combinations_expanded = []
    custom_bindings_names = []
    combination_exists = False

    cmd = "gsettings" + " " + "list-recursively" + " " + CUSTOM_KEYS_PARENT_SCHEMA
    output = get_output(cmd)

    output_lines = output.splitlines()
    #print(line_array)
    #TODO: check if anything found
    pattern = "\[.+?]"
    has_custom_list = False
    non_custom_keys_list = []
    for aline in output_lines:
        if ' custom-list ' in aline:
            tmp = re.findall(pattern, aline, flags=0)
            custom_bindings_names = eval(tmp[-1])
            has_custom_list = True
            continue

        tmp = re.findall(pattern, aline, flags=0)
        if len(tmp):
            #split array of combinations in case more then one exists
            many_combinations = eval(tmp[-1])
            for acombination in many_combinations:
                key_combinations_bundled.append(acombination)

    if has_custom_list:
        for acustom in custom_bindings_names:
            cmd = "gsettings" + " " + "get" + " " + CUSTOM_KEYS_SCHEMA + ":" + CUSTOM_KEYS_BASENAME + "/" + acustom + "/  binding"
            output = get_output(cmd)
            #returns a single arraylike string
            many_combinations = eval(output)
            #print(output,'output')
            #print(many_combinations,'many_combinations')
            for acombination in many_combinations:
                key_combinations_bundled.append(acombination)

    my_specialkeys, my_simplekey = extract_key_combinations_from_string(my_combination)
    for acombination in key_combinations_bundled:
        thespecialkeys, thesimplekey = extract_key_combinations_from_string(acombination)
        if sorted(thespecialkeys) == sorted(my_specialkeys) and thesimplekey == my_simplekey:
            combination_exists = True
    return key_combinations_bundled, custom_bindings_names, combination_exists


def bind_shortcut_to_command(thepath, existingnames, my_combination=DEFAULT_KEY_COMBINATION):
    prefix = "custom"

    # make sure the additional keybinding mention is no duplicate
    xcounter = 1
    while True:
        new = prefix + str(xcounter)
        if new in existingnames:
            xcounter += 1
        else:
            break
    shortcut_name = prefix + str(xcounter)
    existingnames.append(shortcut_name)
    # create the shortcut, set the name, command and shortcut key
    cmd0 = 'gsettings set '+ CUSTOM_KEYS_PARENT_SCHEMA +' custom-list "'+str(existingnames)+'"'
    cmd1 = "gsettings" + " " + "set" + " " + CUSTOM_KEYS_SCHEMA + ":" + CUSTOM_KEYS_BASENAME + "/" + shortcut_name + '/  name "disable-enable synaptics touchpad"'
    cmd2 = "gsettings" + " " + "set" + " " + CUSTOM_KEYS_SCHEMA + ":" + CUSTOM_KEYS_BASENAME + "/" + shortcut_name + '/  command "' + thepath + '"'
    cmd3 = "gsettings" + " " + "set" + " " + CUSTOM_KEYS_SCHEMA + ":" + CUSTOM_KEYS_BASENAME + "/" + shortcut_name + '/  binding "[\'' + my_combination + '\']"'

    for cmd in [cmd0, cmd1, cmd2, cmd3]:
        output = get_output(cmd)

#key
def cinnamon_add_custom_setting(thecommand, my_combination=DEFAULT_KEY_COMBINATION, descriptive_name = 'disable-enable synaptics touchpad'):
    parent_shema = Gio.Settings.new(CUSTOM_KEYS_PARENT_SCHEMA)
    custom_list_array = parent_shema.get_strv("custom-list")

    prefix = "custom"

    # make sure the additional keybinding mention is no duplicate
    xcounter = 1
    while True:
        new = prefix + str(xcounter)
        if new in custom_list_array:
            xcounter += 1
        else:
            break
    shortcut_name = prefix + str(xcounter)

    #new_str = "custom" + str(custom_num)
    custom_list_array.append(shortcut_name)
    parent_shema.set_strv("custom-list", custom_list_array)
    new_path = CUSTOM_KEYS_BASENAME + "/" + shortcut_name + "/"
    new_schema = Gio.Settings.new_with_path(CUSTOM_KEYS_SCHEMA, new_path)
    new_schema.delay()
    new_schema.set_string("name", descriptive_name)
    new_schema.set_string("command",thecommand)
    new_schema.set_strv("binding",[my_combination])
    new_schema.apply()
    Gio.Settings.sync()

def pkill_a_process(process_name):

    try:
        output = subprocess.getoutput("pkill " + process_name)
        return str(output)
    except Exception as e:
        return str(e)


class GetSynapticsShortCut:
    def __init__(self):
        #self.test = 0
        pass


    def get_xinput_list(self):
        xinput_list = subprocess.getoutput("xinput --list --name-only")
        return xinput_list

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

