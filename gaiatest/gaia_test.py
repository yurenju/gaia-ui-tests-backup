# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase
from marionette import Marionette
from marionette import MarionetteTouchMixin
from marionette.errors import NoSuchElementException
from marionette.errors import ElementNotVisibleException
from marionette.errors import TimeoutException
import os
import time


class LockScreen(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_lock_screen.js"))
        self.marionette.import_script(js)

    def lock(self):
        return self.marionette.execute_async_script("GaiaLockScreen.lock()")

    def unlock(self):
        return self.marionette.execute_async_script("GaiaLockScreen.unlock()")


class GaiaApp(object):

    def __init__(self, origin=None, name=None, frame_id=None, src=None):
        self.frame_id = frame_id
        self.src = src
        self.name = name
        self.origin = origin


class GaiaApps(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_apps.js"))
        self.marionette.import_script(js)

    def launch(self, name, switch_to_frame=True, url=None):
        result = self.marionette.execute_async_script("GaiaApps.launchWithName('%s')" % name)
        app = GaiaApp(frame_id=result.get('frame'),
                      src=result.get('src'),
                      name=result.get('name'),
                      origin=result.get('origin'))
        if app.frame_id is None:
            raise Exception("App failed to launch; there is no app frame")
        if switch_to_frame:
           self.switch_to_frame(app.frame_id, url) 
        return app

    def uninstall(self, name):
        self.marionette.execute_async_script("GaiaApps.uninstallWithName('%s')" % name)

    def kill(self, app):
        self.marionette.switch_to_frame()
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_apps.js"))
        self.marionette.import_script(js)
        self.marionette.execute_script("window.wrappedJSObject.WindowManager.kill('%s');"
                                       % app.origin)

    def kill_all(self):
        self.marionette.switch_to_frame()
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_apps.js"))
        self.marionette.import_script(js)
        self.marionette.execute_async_script("GaiaApps.killAll()")

    def runningApps(self):
        apps = self.marionette.execute_script("""
return window.wrappedJSObject.WindowManager.getRunningApps();
            """)
        return apps

    def switch_to_frame(self, app_frame, url=None, timeout=30):
        self.marionette.switch_to_frame(app_frame)
        start = time.time()
        if not url:
            def check(now):
                return "about:blank" not in now
        else:
            def check(now):
                return url in now
        while (time.time() - start < timeout):
            if check(self.marionette.get_url()):
                return
            time.sleep(2)
        raise TimeoutException('Could not switch to app frame %s in time' % app_frame)

class GaiaData(object):

    def __init__(self, marionette):
        self.marionette = marionette
        js = os.path.abspath(os.path.join(__file__, os.path.pardir, 'atoms', "gaia_data_layer.js"))
        self.marionette.import_script(js)
        self.marionette.set_search_timeout(10000)

    def insert_contact(self, contact):
        self.marionette.execute_script("GaiaDataLayer.insertContact(%s)" % contact.json())

    def remove_contact(self, contact):
        self.marionette.execute_script("GaiaDataLayer.findAndRemoveContact(%s)" % contact.json())

    def set_volume(self, volume):
        self.marionette.execute_script("GaiaDataLayer.setVolume(%s)" % volume)

    def enable_wifi(self):
        self.marionette.execute_script("return GaiaDataLayer.enableWifi()")

    def disable_wifi(self):
        self.marionette.execute_script("return GaiaDataLayer.disableWifi()")

    def connect_to_wifi(self, ssid):
        self.marionette.execute_script("return GaiaDataLayer.connectToWiFI('%s')" % ssid)

    def forget_wifi(self, ssid):
        self.marionette.execute_script("return GaiaDataLayer.forgetWiFI('%s')" % ssid)

class GaiaTestCase(MarionetteTestCase):

    def setUp(self):
        MarionetteTestCase.setUp(self)
        self.marionette.__class__ = type('Marionette', (Marionette, MarionetteTouchMixin), {})
        self.marionette.setup_touch()

        # the emulator can be really slow!
        self.marionette.set_script_timeout(60000)
        self.lockscreen = LockScreen(self.marionette)
        self.apps = GaiaApps(self.marionette)
        self.data_layer = GaiaData(self.marionette)

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

    def wait_for_condition(self, method, timeout=10,
                           message="Condition timed out"):
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
        self.data_layer = None
        MarionetteTestCase.tearDown(self)
