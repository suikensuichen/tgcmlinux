#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Authors : Roberto Majadas <roberto.majadas@openshine.com>
#           Oier Blasco <oierblasco@gmail.com>
#           Alvaro Peña <alvaro.pena@openshine.com>
#
# Copyright (c) 2003-2012, Telefonica Móviles España S.A.U.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import webbrowser

import tgcm
import tgcm.core.Theme

import tgcm.ui
import tgcm.ui.MSD

class MSDAInternet(tgcm.ui.MSD.MSDAction):
    def __init__(self):
        tgcm.info("Init MSDAInternet")
        tgcm.ui.MSD.MSDAction.__init__(self, "internet")

        theme_manager = tgcm.core.Theme.ThemeManager()
        self.taskbar_icon_name = 'internet_taskbar.png'
        self.window_icon_path = theme_manager.get_icon('icons', self.taskbar_icon_name)

        self.browser_by_default_checkbutton = self.get_prefs_widget("browser_by_default_checkbutton")
        self.initial_webpage_entry = self.get_prefs_widget("initial_webpage_entry")

        if self._get_conf_key_value("url") is not None:
            self.initial_webpage_entry.set_text(self._get_conf_key_value("url"))

        if self._get_conf_key_value("open_browser_by_default") == True :
            self.browser_by_default_checkbutton.set_active(True)
        else:
            self.browser_by_default_checkbutton.set_active(False)
            self.initial_webpage_entry.set_sensitive(False)

        self.browser_by_default_checkbutton.connect("toggled", self.__browser_checkbutton_cb, None)
        self.initial_webpage_entry.connect("changed", self.__initial_webpage_entry_cb, None)

    def __browser_checkbutton_cb (self, widget, data):
        if self.browser_by_default_checkbutton.get_active() == True :
            self._set_conf_key_value("open_browser_by_default", True)
            self.initial_webpage_entry.set_sensitive(True)
        else:
            self._set_conf_key_value("open_browser_by_default", False)
            self.initial_webpage_entry.set_sensitive(False)

    def __initial_webpage_entry_cb(self, widget, data):
        self._set_conf_key_value("url", self.initial_webpage_entry.get_text())

    def launch_action(self, params=None):
        if self._get_conf_key_value("open_browser_by_default") == True:
            url = self._get_conf_key_value("url")
            if url.startswith ("http"):
                webbrowser.open(url)
            else:
                webbrowser.open("http://%s " % url)
