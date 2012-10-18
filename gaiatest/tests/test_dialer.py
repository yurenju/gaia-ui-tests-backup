# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestDialer(GaiaTestCase):

    _remote_phone = ""

    _keyboard_container_locator = ('id', 'keyboard-container')
    _phone_number_view_locator = ('id', 'phone-number-view')
    _call_bar_locator = ('id', 'keypad-callbar-call-action')
    _hangup_bar_locator = ('id', 'callbar-hang-up-action')
    _call_screen_locator = ('id', 'call-screen')

    # TODO incomplete requires bug 800011
    @unittest.skipIf(self.test_vars['remote_phone_number']
        is "", "Cannot complete test without a remote phone")
    def incomplete_dialer_make_call(self):
        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        app = self.apps.launch('Dialer')
        self.assertTrue(app.frame_id is not None)

        # switch into the app's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('dialer' in url, 'wrong url: %s' % url)

        self.wait_for_element_displayed(*self._keyboard_container_locator)

        self.dial_number(self._remote_phone)

        # Assert that the number was entered correctly.
        phone_view = self.marionette.find_element(*self._phone_number_view_locator).text
        self.assertTrue(phone_view.text, self._remote_phone)

        # Now press call
        self.marionette.find_element(*self._call_bar_locator).click()

        # TODO Need to work out here how to get and switch to new window

        # Wait for call screen
        self.wait_for_element_displayed(*self._call_screen_locator)

        # TODO assert that it is ringing

        # hang up
        self.marionette.find_element(*self._hangup_bar_locator).click()

        # close the app
        self.apps.kill(app)


    def dial_number(self, phone_number):
        '''
        Dial a number using the keypad
        '''

        # TODO Doesn't work for + yet, requires click/hold gestures
        for i in phone_number:
            if i == "+": continue
            self.marionette.find_element('css selector', 'div.keypad-key div[data-value="%s"]' % i).click()
            time.sleep(0.5)
