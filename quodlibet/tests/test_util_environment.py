# -*- coding: utf-8 -*-
# Copyright 2015 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

from tests import TestCase

from quodlibet.util.environment import is_unity


class TUtilEnvironment(TestCase):

    def test_is_unity(self):
        self.assertTrue(isinstance(is_unity(), bool))
