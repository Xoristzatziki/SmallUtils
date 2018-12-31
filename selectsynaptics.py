#!/usr/bin/env python3
#FIXME:
# This is an example class generated using a bare glade file.
#
#FIXME:
"""
    Copyright (C) ilias iliadis, 2018-12-25; ilias iliadis <>

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
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox
except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

settings = None # Keep window related options
options = None #Keep application wide options in a 'General Options' section

class SelectSynaptics(Gtk.ApplicationWindow):
    #FIXME: fix the docstring.
    """ Main window with all components. """

    def __init__(self, *args, **kwargs):
        # Set the app
        self.myparent = None
        if 'parent' in kwargs:#use the same application
            self.myparent = kwargs['parent']
        if 'app' in kwargs:#use the application
            self.app = kwargs['parent'].app
        elif 'application' in kwargs:
            self.app = kwargs['application']
        #this has problems
        if self.myparent and 'modal' in kwargs:
            # "modal" means caller require transient
            self.set_transient_for(self.myparent)
            # but modality can be false, and parent may not be present
            if self.myparent:
                self.set_modal(kwargs['modal'])
        self.custom_args = {}
        if 'custom_args' in kwargs:
            self.custom_args = {k:v for k,v in kwargs['custom_args'].items()}
            # do not pass them to Gtk.ApplicationWindow init
            # otherwise will trigger an error
            del kwargs['custom_args']
            if 'trigger_before_exit' in self.custom_args:
                # must be a function on calling class
                self.trigger_before_exit = self.custom_args['trigger_before_exit']
                self.return_parameters = None

        self.return_parameters = {}
        # Before super initialization.

        # init super.
        # First init the window, otherwise MRO will mess it.
        Gtk.ApplicationWindow.__init__(self, *args, **kwargs)

        # Any nitializations required before loading the glade file.

        # Now load builder.
        self._get_from_builder()

        # Load any settings or run extra initializations.
        self._post_initialisations()

#********* Auto created "class defs" START ************************************************************
    def _get_from_builder(self):
        """ Load components from a glade file. """
        # Load the ui from a glade file.
        self.builder = Gtk.Builder()
        try:
            self.builder.add_from_file(os.path.join(self.app.BASE_DIR,
                'ui',
                'selectsynaptics.glade')
            )
        except Exception as ex:
            print(str(ex))
            print('\n{}:\n{}\n{}'.format(_('Error loading from Glade file'),
                os.path.join(self.app.BASE_DIR,
                'ui',
                'selectsynaptics.glade'), repr(ex))
            )
            sys.exit(ERROR_INVALID_GLADE_FILE)

        # Get gui objects.
        self.boxForFooter = self.builder.get_object('boxForFooter')
        self.boxMain = self.builder.get_object('boxMain')
        self.buttonCancel = self.builder.get_object('buttonCancel')
        self.buttonOK = self.builder.get_object('buttonOK')
        self.comboboxtextDevices = self.builder.get_object('comboboxtextDevices')
        self.label1 = self.builder.get_object('label1')
        self.labelSelected = self.builder.get_object('labelSelected')
        self.labelWarning = self.builder.get_object('labelWarning')

        # Connect signals existing in the Glade file.
        self.builder.connect_signals(self)

        # Reparent our main container from glader file,
        # this way we have all Gtk.Window functionality using "self".
        thechild = self.builder.get_object('windowMain').get_child()
        thechild.get_parent().remove(thechild)
        self.add(thechild)

        # Connect generated signals:
        # top window signals and/or other generated signals.
        # top window signals were connected, by builder's "connect_signals" function,
        # to builder's main window
        self.connect('delete-event', self.on_windowMain_delete_event)
        self.connect('destroy', self.on_windowMain_destroy)
        self.connect('size-allocate', self.on_windowMain_size_allocate)
        self.connect('window-state-event', self.on_windowMain_window_state_event)


        # :builder top window properties.
        self.can_focus = 'False'

        # Load window icon from app, if any.
        self.set_icon(self.app.icon)

    def _post_initialisations(self):
        """ Do some extra initializations.

        Display the version if a labelVersion is found.
        Set defaults (try to load them from a configuration file):
            - Window size and state (width, height and if maximized)
        Load saved custom settings.
        """
        # Init the settings module.
        self.dummy_for_settings = SectionConfig(self.app.id, self.__class__.__name__)
        global settings
        settings = self.dummy_for_settings

        self.dummy_for_options = OptionConfig(self.app.id)
        global options
        options = self.dummy_for_options

        # Bind message boxes.
        self.MessageBox = MessageBox(self)
        self.msg = self.MessageBox.Message
        self.are_you_sure = self.MessageBox.are_you_sure

        # Set previous size and state.
        width = settings.get('width', 350)
        height = settings.get('height', 350)
        self.set_title(self.app.localizedname)
        self.resize(width, height)
        if settings.get_bool('maximized', False):
            self.maximize()
        # Load any other settings here.
        self.load_xinput_devices()

#********* Auto created handlers START *********************************
    def on_buttonCancel_clicked(self, widget, *args):
        """ Handler for buttonCancel.clicked. """
        self.return_parameters['has selection'] = False
        self.exit_requested()

    def on_buttonOK_clicked(self, widget, *args):
        """ Handler for buttonOK.clicked. """
        self.return_parameters['selected'] = self.comboboxtextDevices.get_active_text()
        self.return_parameters['has selection'] = True
        self.exit_requested()

    def on_comboboxtextDevices_changed(self, widget, *args):
        """ Handler for comboboxtextDevices.changed. """
        self.labelSelected.set_label(self.comboboxtextDevices.get_active_text())
        self.buttonOK.set_sensitive(self.comboboxtextDevices.get_active() > 0)

    def on_windowMain_delete_event(self, widget, event, *args):
        """ Handler for windowMain.delete-event. """
        return (self.exit_requested('from_delete_event'))

    def on_windowMain_destroy(self, widget, *args):
        """ Handler for windowMain.destroy. """
        return (self.exit_requested('from_destroy'))

    def on_windowMain_size_allocate(self, widget, allocation, *args):
        """ Handler for windowMain.size-allocate. """
        self.save_my_size()

    def on_windowMain_window_state_event(self, widget, event, *args):
        """ Handler for windowMain.window-state-event. """
        settings.set('maximized',
            ((int(event.new_window_state) & Gdk.WindowState.ICONIFIED) != Gdk.WindowState.ICONIFIED) and
            ((int(event.new_window_state) & Gdk.WindowState.MAXIMIZED) == Gdk.WindowState.MAXIMIZED)
            )
        self.save_my_size()


#********* Auto created handlers  END **********************************

    def exit_requested(self, *args, **kwargs):
        """ Final work before exit. """
        self.set_transient_for()
        self.set_modal(False)
        self.set_unhandled_settings()# also saves all settings
        if 'from_destroy' in args or 'from_delete_event' in args:
            return True
        else:
            # Check if we should provide info to caller
            if 'trigger_before_exit' in self.custom_args:
                self.trigger_before_exit(exiting = True,
                    return_parameters = self.return_parameters)
            self.destroy()

    def present(self):
        """ Show the window. """
        self.show_all()
        #"enable" next line to have some interactive view of potentiallities of GUI
        #self.set_interactive_debugging (True)
        super().present()

    def save_my_size(self):
        """ Save the window size into settings, if not maximized. """
        if not settings.get_bool('maximized', False):
            width, height = self.get_size()
            settings.set('width', width)
            settings.set('height', height)

    def set_unhandled_settings(self):
        """ Set, before exit, settings not applied during the session.

        Additionally, flush all settings to .conf file.
        """
        # Set any custom settings
        # which where not setted (ex. on some widget's state changed)

        # Save all settings
        settings.save()

#********* Auto created "class defs" END **************************************************************
    def load_xinput_devices(self):
        xinput_list = subprocess.getoutput("xinput --list --name-only")
        devices_list = xinput_list.splitlines()
        self.comboboxtextDevices.remove_all()
        self.comboboxtextDevices.append_text(_("---Please select one---"))
        for aninputdevice in devices_list:
            self.comboboxtextDevices.append_text(aninputdevice)
        self.comboboxtextDevices.set_active(0)

#********* Window class  END***************************************************************************
