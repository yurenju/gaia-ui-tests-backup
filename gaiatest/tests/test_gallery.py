# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from subprocess import call
import time
import sys

class TestGallery(GaiaTestCase):

    def test_calculator_basic(self):
        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())
        # launch the Gallery app
        app = self.apps.launch('Gallery')
