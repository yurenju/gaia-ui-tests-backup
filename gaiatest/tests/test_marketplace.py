# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestMarketplace(GaiaTestCase):

    _login_button = ('css selector', 'p.proceed > a.button.browserid')



    # TODO incomplete - this test requires Bug 802227
    def incomplete_load_marketplace(self):
        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        app = self.apps.launch('Marketplace')
        self.assertTrue(app.frame_id is not None)

        # switch into the app's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('marketplace' in url, 'wrong url: %s' % url)

        # TODO replace this with an appropriate wait
        time.sleep(10)

        self.marionette.find_element(*self._login_button).click()

        time.sleep(10)

        #TODO switch to Persona frame

        #TODO complete Persona login

        #TODO verify that user is logged in

        # close the app
        self.apps.kill(app)
