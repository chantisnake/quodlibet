# -*- coding: utf-8 -*-
# Copyright 2007 Joe Wreschnig
#
# This software and accompanying documentation, if any, may be freely
# used, distributed, and/or modified, in any form and for any purpose,
# as long as this notice is preserved. There is no warranty, either
# express or implied, for this software.

import os
from distutils.dep_util import newer

from .util import Command
from .gettextutil import intltool


class build_shortcuts(Command):
    """Build .desktop files

    Move .desktop files to the appropriate location in the build tree.
    If there is a .desktop.in file, process it with intltool.
    """

    description = "build .desktop files"
    user_options = []

    def initialize_options(self):
        self.build_base = None

    def finalize_options(self):
        self.shortcuts = self.distribution.shortcuts
        self.po_directory = self.distribution.po_directory
        self.set_undefined_options('build', ('build_base', 'build_base'))

    def __check_po(self):
        """Exit if translation is needed and not available"""
        if not (self.po_directory and os.path.isdir(self.po_directory)):
            raise SystemExit("PO directory %r not found." % self.po_directory)

    def run(self):
        basepath = os.path.join(self.build_base, 'share', 'applications')
        self.mkpath(basepath)
        for shortcut in self.shortcuts:
            if os.path.exists(shortcut + ".in"):
                fullpath = os.path.join(basepath, os.path.basename(shortcut))
                self.__check_po()
                if newer(shortcut + ".in", fullpath):
                    self.spawn(
                        intltool("merge", "-d", self.po_directory,
                                 shortcut + ".in", fullpath))
            else:
                self.copy_file(shortcut, os.path.join(basepath, shortcut))


class install_shortcuts(Command):
    """Install .desktop files

    Install any .desktop files from the build tree to their final
    location, under $prefix/share/applications.
    """

    description = "install .desktop files"
    user_options = []

    def initialize_options(self):
        self.install_dir = None
        self.skip_build = None
        self.shortcuts = None
        self.build_base = None
        self.outfiles = []

    def finalize_options(self):
        self.set_undefined_options('build', ('build_base', 'build_base'))
        self.set_undefined_options(
            'install',
            ('install_data', 'install_dir'),
            ('skip_build', 'skip_build'))

        self.set_undefined_options(
            'build_shortcuts', ('shortcuts', 'shortcuts'))

    def get_outputs(self):
        return self.outfiles

    def run(self):
        if not self.skip_build:
            self.run_command('build_shortcuts')
        basepath = os.path.join(self.install_dir, 'share', 'applications')
        srcpath = os.path.join(self.build_base, 'share', 'applications')
        out = self.mkpath(basepath)
        self.outfiles.extend(out or [])
        for shortcut in self.shortcuts:
            shortcut = os.path.basename(shortcut)
            fullsrc = os.path.join(srcpath, shortcut)
            fullpath = os.path.join(basepath, shortcut)
            (out, _) = self.copy_file(fullsrc, fullpath)
            self.outfiles.append(out)

__all__ = ["build_shortcuts", "install_shortcuts"]
