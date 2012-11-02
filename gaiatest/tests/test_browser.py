# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time
import unittest


class TestBrowser(GaiaTestCase):

    _awesome_bar_locator = ("id", "url-input")
    _url_button_locator = ("id", "url-button")
    _throbber_locator = ("id", "throbber")
    _browser_frame_locator = ('css selector', 'iframe[mozbrowser]')
    _browser_bookmark_button = ("id", "bookmark-button")
    _browser_add_to_home_button = ("id", "bookmark-menu-add-home")
    _homescreen_add_to_home_button = ("id", "button-bookmark-add")

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        self.home = self.apps.launch('Homescreen')
        self.app = self.apps.launch('Browser')
        self.assertTrue(self.app.frame_id is not None)

        # switch into the app's frame
        self.marionette.switch_to_frame(self.app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('browser' in url, 'wrong url: %s' % url)

    @unittest.skip("Don't want to run this on CI")
    def test_browser_basic(self):
        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        awesome_bar.click()
        awesome_bar.send_keys("www.mozilla.com")

        self.marionette.find_element(*self._url_button_locator).click()

        # This is returning True even though I cannot see it
        self.wait_for_condition(lambda m: self.is_throbber_visible() == False)

        # TODO This does not work
        browser_frame = self.marionette.find_element(
            *self._browser_frame_locator)
        print browser_frame

        self.marionette.switch_to_frame(browser_frame)

        # TODO
        # Assert that the page has loaded correctly
        # Assert the error page is not shown
    def test_browser_add_to_homescreen(self):
        awesome_bar = self.marionette.find_element(*self._awesome_bar_locator)
        bookmark_button = self.marionette.find_element(
            *self._browser_bookmark_button)
        browser_add_to_home_button = self.marionette.find_element(
            *self._browser_add_to_home_button)

        awesome_bar.click()
        awesome_bar.send_keys("www.mozilla.com")
        self.marionette.find_element(*self._url_button_locator).click()
        self.wait_for_element_displayed(*self._browser_bookmark_button)
        bookmark_button.click()
        browser_add_to_home_button.click()

        self.marionette.switch_to_frame(self.home.frame_id)
        self.wait_for_element_displayed(*self._homescreen_add_to_home_button)
        homescreen_add_to_home_button = self.marionette.find_element(
            *self._homescreen_add_to_home_button)
        homescreen_add_to_home_button.click()

    def tearDown(self):

        # close the app
        if hasattr(self, 'app'):
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)

    def is_throbber_visible(self):
        return self.marionette.find_element(*self._throbber_locator).size['height'] == 4
