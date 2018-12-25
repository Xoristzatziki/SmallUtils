#!/usr/bin/env python3
#FIXME:
# This is an example class generated using a bare glade file.
#
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

WARNING_SYNAPTICS = """WARNING!!!!!

The program does not check if the keyboard shortcut binding exists.
If the shortcut:
{}
is binded to another command you may encounter problems.

You have been warned.

"""
try:
    import os
    import sys

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
    from auxiliary2 import ChooserDialog
    from auxiliary2 import RemoveDS_Storefiles
    from auxiliary2 import RemoveExecutableFromFiles
    import auxiliary2 as other_functions
    #from auxiliary2 import SetSynapticsShortCut
    from selectsynaptics import SelectSynaptics

except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

settings = None # Keep window related options
options = None #Keep application wide options in a 'General Options' section

class StartWindow(Gtk.ApplicationWindow):
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
                'startwindow.glade')
            )
        except Exception as ex:
            print(str(ex))
            print('\n{}:\n{}\n{}'.format(_('Error loading from Glade file'),
                os.path.join(self.app.BASE_DIR,
                'ui',
                'startwindow.glade'), repr(ex))
            )
            sys.exit(ERROR_INVALID_GLADE_FILE)

        # Get gui objects.
        self.boxCommands = self.builder.get_object('boxCommands')
        self.boxCreateSynapticsShortcut = self.builder.get_object('boxCreateSynapticsShortcut')
        self.boxForFooter = self.builder.get_object('boxForFooter')
        self.boxMain = self.builder.get_object('boxMain')
        self.boxRemoveDS_Store = self.builder.get_object('boxRemoveDS_Store')
        self.boxRemoveExecutable = self.builder.get_object('boxRemoveExecutable')
        self.buttonAbout = self.builder.get_object('buttonAbout')
        self.buttonExit = self.builder.get_object('buttonExit')
        self.buttonRemoveDS_Store = self.builder.get_object('buttonRemoveDS_Store')
        self.buttonRemoveExecutable = self.builder.get_object('buttonRemoveExecutable')
        self.buttonSynaptics = self.builder.get_object('buttonSynaptics')
        self.dummylabel = self.builder.get_object('dummylabel')
        self.eventboxPathRemoveDS_Store = self.builder.get_object('eventboxPathRemoveDS_Store')
        self.eventboxPathRemoveExecutable = self.builder.get_object('eventboxPathRemoveExecutable')
        self.eventboxSynaptics = self.builder.get_object('eventboxSynaptics')
        self.label1 = self.builder.get_object('label1')
        self.label2 = self.builder.get_object('label2')
        self.label3 = self.builder.get_object('label3')
        self.labelPathRemoveDS_Store = self.builder.get_object('labelPathRemoveDS_Store')
        self.labelPathRemoveExecutable = self.builder.get_object('labelPathRemoveExecutable')
        self.labelSynaptics = self.builder.get_object('labelSynaptics')
        self.labelVersion = self.builder.get_object('labelVersion')
        self.labeltest = self.builder.get_object('labeltest')

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
        self.buttonRemoveDS_Store.connect('clicked', self.on_buttonRemoveDS_Store_clicked)
        self.buttonRemoveExecutable.connect('clicked', self.on_buttonRemoveExecutable_clicked)
        self.buttonSynaptics.connect('clicked', self.on_buttonSynaptics_clicked)
        self.connect('delete-event', self.on_windowMain_delete_event)
        self.connect('destroy', self.on_windowMain_destroy)
        self.connect('size-allocate', self.on_windowMain_size_allocate)
        self.connect('window-state-event', self.on_windowMain_window_state_event)


        # :builder top window properties.
        # Set the label for labelVersion
        self.labelVersion.set_label(VERSIONSTR)
        self.labelVersion.set_tooltip_text(_("""This is the version of this window.
Not the version of the application."""))
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

        self.synaptics_device = None


#********* Auto created handlers START *********************************
    def on_buttonAbout_clicked(self, widget, *args):
        """ Handler for buttonAbout.clicked. """
        self.MessageBox.AboutBox()

    def on_buttonExit_clicked(self, widget, *args):
        """ Handler for buttonExit.clicked. """
        self.exit_requested()

    def on_buttonRemoveDS_Store_clicked(self, widget, *args):
        """ Handler for buttonRemoveDS_Store.clicked. """
        fullpath = self.labelPathRemoveDS_Store.get_tooltip_text()
        if fullpath and os.path.exists(fullpath):
            msg = _('This will remove .DS_Store files, recursively, inside the directory:\n{}\n')
            msg += _('Proceed?')
            ok  = self.msg(msg.format(fullpath,), buttons='YESCANCEL', boxtype = 'QUESTION')
            if ok:
                result = RemoveDS_Storefiles(fullpath)
                self.labelPathRemoveDS_Store.set_label('')
                self.labelPathRemoveDS_Store.set_tooltip_text('')
        else:
            self.msg('No valid path!' + '\n' + str(fullpath))

    def on_buttonRemoveExecutable_clicked(self, widget, *args):
        """ Handler for buttonRemoveExecutable.clicked. """
        fullpath = self.labelPathRemoveExecutable.get_tooltip_text()
        if fullpath and os.path.exists(fullpath):
            msg = _('This will remove executable from files, recursively, inside the directory:\n{}\n')
            msg += _('Proceed?')
            ok  = self.msg(msg.format(fullpath,), buttons='YESNOCANCEL', boxtype = 'WARNING')
            if ok:
                msg = _('This may make programs to stop responding!\n')
                msg += _('Are you sure?')
                ok  = self.msg(msg.format(fullpath,), buttons='YESCANCEL', boxtype = 'QUESTION')
                if ok:
                    result = RemoveExecutableFromFiles(fullpath)
                    self.labelPathRemoveExecutable.set_label('')
                    self.labelPathRemoveExecutable.set_tooltip_text('')
        else:
            self.msg('No valid path!' + '\n' + str(fullpath))

    def on_buttonSynaptics_clicked(self, widget, *args):
        """ Handler for buttonSynaptics.clicked. """

        if self.synaptics_device == None:
            self.msg(_("No device selected!"))
            return

        OR_WAIT = _("You must manually alter it \nor wait for the version that will do this automatically.")
        key_combinations_bundled, custom_bindings_names, combination_exists = other_functions.get_shorcut_combinations()
        if combination_exists:
            self.msg(_('The default combination already exists.\n') + OR_WAIT)
            return

        my_bin_path = os.path.expanduser("~/bin")
        disable_synaptics_path = os.path.join(my_bin_path,"my_disable_synaptics")
        if os.path.exists(disable_synaptics_path):
            self.msg(_('The default bash script already exists.\n') + OR_WAIT)
            return
        thescripttext  = other_functions.create_synaptics_bash_file(self.synaptics_device)
        try:
            with open(disable_synaptics_path, 'x', encoding='utf-8') as f:
                f.write(thescripttext)
        except Exception as e:
            print("An exception occured.", e)
        make_executable(disable_synaptics_path)
        #other_functions.bind_shortcut_to_command(disable_synaptics_path, custom_bindings_names)
        other_functions.cinnamon_add_custom_setting(disable_synaptics_path)

        self.buttonSynaptics.set_sensitive(False)
        self.eventboxSynaptics.set_sensitive(False)
        msg = _("""A key binding to a newly created script has been created.""")

        self.msg(msg)

    def on_eventboxPathRemoveDS_Store_button_release_event(self, widget, event, *args):
        """ Handler for eventboxPathRemoveDS_Store.button-release-event. """
        dlg = ChooserDialog()
        thepath = dlg.select_folder(self)
        if thepath:
            head, tail = os.path.split(thepath)
            self.labelPathRemoveDS_Store.set_label(tail + '\n' + head)
            self.labelPathRemoveDS_Store.set_tooltip_text(thepath)

    def on_eventboxPathRemoveExecutable_button_press_event(self, widget, event, *args):
        """ Handler for eventboxPathRemoveExecutable.button-press-event. """
        dlg = ChooserDialog()
        thepath = dlg.select_folder(self)
        if thepath:
            head, tail = os.path.split(thepath)
            self.labelPathRemoveExecutable.set_label(tail + '\n' + head)
            self.labelPathRemoveExecutable.set_tooltip_text(thepath)

    def on_eventboxSynaptics_button_press_event(self, widget, event, *args):
        """ Handler for eventboxSynaptics.button-press-event. """
        some_custom_args = {}
        some_custom_args['modal'] = True
        #event to trigger on return
        some_custom_args['trigger_before_exit'] = self.synaptice_device_selected
        #print(type(self.eventboxSynaptics.get_toplevel().super()))
        self.synaptics_select = SelectSynaptics(application=self.app,
                #parent = self.eventboxSynaptics.get_toplevel(),
                custom_args = some_custom_args,
                modal = True)
        self.hide()
        self.synaptics_select.present()


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
    def synaptice_device_selected(self, *args, **kwargs):
        #print(args)
        #print(kwargs)
        return_parameters = kwargs['return_parameters']
        if return_parameters['has selection']:
            self.labelSynaptics.set_markup(_("Selected device") + ":\n<b>" + return_parameters['selected'] + "</b>")
            self.synaptics_device = return_parameters['selected']
        else:
            self.labelSynaptics.set_markup("<b>" + _("No device selected!!!") + "</b>")
            self.synaptics_device = None
        self.show()


#********* Window class  END***************************************************************************
def make_executable(filename):
    """ Make a file executable, by setting mode 774. """
    import stat
    # chmod 774
    mode774 = stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH
    os.chmod(filename, mode774)
