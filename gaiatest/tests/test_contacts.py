# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestContacts(GaiaTestCase):

    def test_add_new_contact(self):
        # https://moztrap.mozilla.org/manage/case/1309/

        self.assertTrue(self.lockscreen.unlock())

        # launch the Contacts app
        app = self.apps.launch('communications/contacts/')
        self.assertTrue(app.frame_id is not None)

        # switch into the Contact's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('communications' in url, 'wrong url: %s' % url)

        #click Create new contact
        self.marionette.find_element('id', 'add-contact-button').click()

        first_name = "NewFirst"
        last_name = "Contact"
        phone_no = "07011111111"
        email = "tester@mozilla.com"
        street = "101 Testing St"
        zip = "90210"
        city = "London"
        country = "UK"
        comment = "cool dude"

        # Enter data into fields

        self.marionette.find_element('name', 'givenName').send_keys(first_name)
        self.marionette.find_element('name', 'familyName').send_keys(last_name)
        self.marionette.find_element('css selector', "input[placeholder='Phone']").send_keys(phone_no)
        self.marionette.find_element('css selector', "input[placeholder='Email']").send_keys(email)

        self.marionette.find_element('css selector', "input[placeholder='Street']").send_keys(street)
        self.marionette.find_element('css selector', "input[placeholder='Zip code']").send_keys(zip)
        self.marionette.find_element('css selector', "input[placeholder='City']").send_keys(city)
        self.marionette.find_element('css selector', "input[placeholder='Country']").send_keys(country)

        self.marionette.find_element('css selector', "input[placeholder='Comment']").send_keys(comment)

        done_button = self.marionette.find_element('id', 'settings-done')
        self.assertTrue(done_button.is_enabled())
        done_button.click()


        # close the app
        self.apps.kill(app)
