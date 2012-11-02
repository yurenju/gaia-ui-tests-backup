# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase
from marionette.errors import NoSuchElementException
from marionette.errors import ElementNotVisibleException
from marionette.errors import TimeoutException
import os
import time


class LockScreen(object):

    def __init__(self, marionette):
        self.marionette = marionette

    def unlock(self):
        success = self.marionette.execute_async_script("""
let setlock = window.wrappedJSObject.SettingsListener.getSettingsLock();
let obj = {'screen.timeout': 0};
setlock.set(obj);

waitFor(
    function() {
        window.wrappedJSObject.LockScreen.unlock();
        waitFor(
            function() {
                finish(window.wrappedJSObject.LockScreen.locked);
            },
            function() {
                return !window.wrappedJSObject.LockScreen.locked;
            }
        );
    },
    function() {
        return !!window.wrappedJSObject.LockScreen;
    }
);
""")
        return success


class GaiaApp(object):

    def __init__(self, app=None, marionette=None):
        self.marionette = marionette
        if app is None:
            return

        for key in app:
            setattr(self, key, app[key])

    def uninstall(self):
        self.marionette.switch_to_frame()
        js = os.path.abspath(
            os.path.join(__file__, os.path.pardir, "gaia_apps.js"))
        self.marionette.import_script(js)
        return self.marionette.execute_async_script("GaiaApps.uninstall('%s')" % self.name)


class GaiaApps(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(
            os.path.join(__file__, os.path.pardir, "gaia_apps.js"))
        self.marionette.import_script(js)

    def get(self, name):
        self.marionette.switch_to_frame()
        result = self.marionette.execute_async_script(
            "GaiaApps.get('%s')" % name)
        app = GaiaApp(app=result, marionette=self.marionette)
        return app

    def launch(self, name):
        result = self.marionette.execute_async_script(
            "GaiaApps.launchWithName('%s')" % name)
        app = GaiaApp(app=result, marionette=self.marionette)
        return app

    def kill(self, app):
        self.marionette.switch_to_frame()
        js = os.path.abspath(
            os.path.join(__file__, os.path.pardir, "gaia_apps.js"))
        self.marionette.import_script(js)
        self.marionette.execute_script("window.wrappedJSObject.WindowManager.kill('%s');"
                                       % app.origin)

    def get_count(self):
        self.marionette.switch_to_frame()
        js = os.path.abspath(
            os.path.join(__file__, os.path.pardir, "gaia_apps.js"))
        self.marionette.import_script(js)
        return self.marionette.execute_async_script("GaiaApps.getCount()")


class GaiaTestCase(MarionetteTestCase):

    def setUp(self):
        MarionetteTestCase.setUp(self)

        # the emulator can be really slow!
        self.marionette.set_script_timeout(60000)
        self.lockscreen = LockScreen(self.marionette)
        self.apps = GaiaApps(self.marionette)

    @property
    def is_emulator(self):
        return self.marionette.emulator is not None

    def wait_for_element_present(self, by, locator, timeout=10):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                return self.marionette.find_element(by, locator)
            except NoSuchElementException:
                pass
        else:
            raise TimeoutException(
                'Element %s not found before timeout' % locator)

    def wait_for_element_not_present(self, by, locator, timeout=10):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                self.marionette.find_element(by, locator)
            except NoSuchElementException:
                break
        else:
            raise TimeoutException(
                'Element %s still present after timeout' % locator)

    def wait_for_element_displayed(self, by, locator, timeout=10):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                if self.marionette.find_element(by, locator).is_displayed():
                    break
            except NoSuchElementException:
                pass
        else:
            raise TimeoutException(
                'Element %s not visible before timeout' % locator)

    def wait_for_element_not_displayed(self, by, locator, timeout=10):
        timeout = float(timeout) + time.time()

        while time.time() < timeout:
            time.sleep(0.5)
            try:
                if not self.marionette.find_element(by, locator).is_displayed():
                    break
            except NoSuchElementException:
                break
        else:
            raise TimeoutException(
                'Element %s still visible after timeout' % locator)

    def wait_for_condition(self, method, timeout=10):
        """Calls the method provided with the driver as an argument until the \
        return value is not False."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                value = method(self.marionette)
                if value:
                    return value
            except NoSuchElementException:
                pass
            time.sleep(0.5)
            if(time.time() > end_time):
                break
        else:
            raise TimeoutException(message)

    def tearDown(self):
        self.lockscreen = None
        self.apps = None
        MarionetteTestCase.tearDown(self)
