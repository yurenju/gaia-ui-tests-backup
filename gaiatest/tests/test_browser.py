# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestBrowser(GaiaTestCase):

    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")
    _throbber_locator = ("id", "throbber")
    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')

    def test_browser_basic(self):
        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        app = self.apps.launch('Browser')
        self.assertTrue(app.frame_id is not None)

        # switch into the app's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('browser' in url, 'wrong url: %s' % url)

        # This is returning True even though I cannot see it
        print self.marionette.find_element(*self._throbber_locator).is_displayed()

        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        awesome_bar.click()
        awesome_bar.send_keys("www.mozilla.com")

        self.marionette.find_element(*self._url_button_locator).click()

        browser_frame = self.marionette.find_element(*self._browser_frame_locator)

        self.marionette.switch_to_frame(browser_frame)

        # TODO
        # Assert that the page has loaded correctly
        # Assert the error page is not shown

        # close the app
        self.apps.kill(app)
