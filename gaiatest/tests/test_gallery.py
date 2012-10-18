# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time

class TestGallery(GaiaTestCase):

    _throbber_locator = ('id', 'throbber')
    _gallery_items_locator = ('css selector', 'li.thumbnail')
    _current_photo = ('css selector', 'div.currentPhoto img[src]')
    _photos_toolbar_locator = ('id', 'photos-toolbar')

    def test_gallery_view(self):
        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the Gallery app
        app = self.apps.launch('Gallery')
        self.assertTrue(app.frame_id is not None)

        # switch into the Gallery's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('gallery' in url, 'wrong url: %s' % url)

        time.sleep(5)
        # throbber is throbbing forever
        #self.wait_for_element_not_displayed(*self._throbber_locator)

        self.marionette.find_elements(*self._gallery_items_locator)[0].click()

        self.wait_for_element_present(*self._current_photo)
        self.assertTrue(self.marionette.find_element(*self._current_photo).is_displayed())

        # TODO
        # Add steps to view picture full screen
        # TODO
        # Repeat test with landscape orientation

        # close the app
        self.apps.kill(app)
