from gaiatest import GaiaTestCase
import time
import unittest

MANIFEST = 'http://mozqa.com/data/webapps/mozqa.com/manifest.webapp'
NAME = 'Mozilla QA WebRT Tester'
VERSION = '1.0'
DESCRIPTION = 'An app for running web runtime test cases with native applications'

class TestInstallApp(GaiaTestCase):
    _yes_button_locator = ('id', 'permission-yes')
    _icons_locator = ('css selector', '.labelWrapper span')

    def setUp(self):
        GaiaTestCase.setUp(self)
        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())
        self.homescreen = self.apps.launch('Homescreen')
        self.count = self.apps.get_count()
        self.marionette.switch_to_frame(self.homescreen.frame_id)

    def test_install_app(self):
        self.marionette.execute_script(
            'navigator.mozApps.install("%s")' % MANIFEST)
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._yes_button_locator)
        yes = self.marionette.find_element(*self._yes_button_locator)
        yes.click()

        self.app = self.apps.get(NAME)
        self.assertEqual(self.apps.get_count(), self.count + 1)
        self.assertEqual(self.app.version, VERSION)
        self.assertEqual(self.app.description, DESCRIPTION)

        self.marionette.switch_to_frame(self.homescreen.frame_id)
        labels = self.marionette.find_elements(*self._icons_locator)
        matches = [lb for lb in labels if lb.text == NAME]
        self.assertTrue(len(matches) > 0)

    def tearDown(self):
        self.app.uninstall()
        GaiaTestCase.tearDown(self)
