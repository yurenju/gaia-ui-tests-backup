# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from mocks.mock_contact import MockContact

class TestContacts(GaiaTestCase):

    _add_new_contact_button_locator = ('id'', add-contact-button')

    _given_name_field_locator = ('id', 'givenName')
    _family_name_field_locator = ('id', 'familyName')
    _email_field_locator = ('id', "email_#i#")
    _phone_field_locator = ('id', "number_#i#")
    _street_field_locator = ('id', "streetAddress_#i#")
    _zip_code_field_locator = ('id', "postalCode_#i#")
    _city_field_locator = ('id', 'locality_#i#')
    _country_field_locator = ('id', 'countryName_#i#')
    _comment_field_locator = ('id', 'note_#i#')

    _done_button_locator = ('id', 'settings-done')

    # TODO waiting for bug 800011
    def test_add_new_contact(self):
        # https://moztrap.mozilla.org/manage/case/1309/

        self.assertTrue(self.lockscreen.unlock())

        contact = MockContact()

        # launch the Contacts app
        app = self.apps.launch('Contacts')
        self.assertTrue(app.frame_id is not None)

        # switch into the Contact's frame
        self.marionette.switch_to_frame(app.frame_id)
        url = self.marionette.get_url()
        self.assertTrue('communications' in url, 'wrong url: %s' % url)

        #click Create new contact
        self.marionette.find_element(*self._add_new_contact_button_locator).click()

        # Enter data into fields
        self.marionette.find_element(*self._given_name_field_locator).send_keys(contact['first_name'])
        self.marionette.find_element(*self._family_name_field_locator).send_keys(contact['last_name'])
        self.marionette.find_element(*self._phone_field_locator).send_keys(contact['phone_no'])
        self.marionette.find_element(*self._email_field_locator).send_keys(contact['email'])

        self.marionette.find_element(*self._street_field_locator).send_keys(street)
        self.marionette.find_element(*self._zip_code_field_locator).send_keys(contact['zip'])
        self.marionette.find_element(*self._city_field_locator).send_keys(contact['city'])
        self.marionette.find_element(*self._country_field_locator).send_keys(contact['country'])

        self.marionette.find_element(*self._comment_field_locator).send_keys(contact['comment'])

        done_button = self.marionette.find_element(*self._done_button_locator)
        self.assertTrue(done_button.is_enabled())
        done_button.click()

        # close the app
        self.apps.kill(app)
