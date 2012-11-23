from gaiatest import GaiaTestCase
import time
import unittest

MANIFEST = 'http://mozqa.com/data/webapps/mozqa.com/manifest.webapp'
APP_NAME = 'Mozilla QA WebRT Tester'


class TestInstallApp(GaiaTestCase):
    _yes_button_locator = ('id', 'app-install-install-button')
    _icon_labels_locator = ('css selector', '.labelWrapper span')

    def setUp(self):
        GaiaTestCase.setUp(self)
        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())
        self.homescreen = self.apps.launch('Homescreen')

    def test_install_app(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script(
            'navigator.mozApps.install("%s")' % MANIFEST)

        self.wait_for_element_displayed(*self._yes_button_locator)
        yes = self.marionette.find_element(*self._yes_button_locator)
        yes.click()

        self.marionette.switch_to_frame(self.homescreen.frame_id)
        labels = self.marionette.find_elements(*self._icon_labels_locator)
        matches = [lb for lb in labels if lb.text == APP_NAME]
        self.assertTrue(len(matches) > 0)

    def tearDown(self):
        self.apps.uninstall(APP_NAME)
        GaiaTestCase.tearDown(self)
