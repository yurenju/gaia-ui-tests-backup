# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from marionette.keys import Keys


class TestMarketplace(GaiaTestCase):

    _search_button = ('css selector', '.header-button.icon.search.right')
    _search = ('id', 'search-q')

    _search_results_area = ('id', 'search-results')
    _search_result = ('css selector', '#search-results li.item')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # unlock the lockscreen if it's locked
        self.assertTrue(self.lockscreen.unlock())

        # launch the app
        self.app = self.apps.launch('Marketplace')
        self.assertTrue(self.app.frame_id is not None)

        # switch into the app's frame
        self.marionette.switch_to_frame(self.app.frame_id)

        url = self.marionette.get_url()
        self.assertTrue('marketplace' in url, 'wrong url: %s' % url)

    def test_that_searches_for_a_app(self):
        self.wait_for_element_displayed(*self._search_button)
        self.marionette.find_element(*self._search_button).click()

        self.wait_for_element_displayed(*self._search)
        search_box = self.marionette.find_element(*self._search)
        search_box.send_keys('Hypno')
        search_box.send_keys(Keys.RETURN)

        self.wait_for_element_displayed(*self._search_results_area)

        results = self.marionette.find_elements(*self._search_result)

        self.assertGreater(len(results), 0, 'no results found')

    def tearDown(self):

        # close the app
        if self.app:
            self.apps.kill(self.app)

        GaiaTestCase.tearDown(self)
