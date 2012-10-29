/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

var GaiaDataLayer = {

    insertContact: function(cdata){
        var contact = new mozContact();
        //contact.init(cdata);
        contact.init({
            givenName: 'Tom',
            familyName: 'Testing',
            name: 'Tom Testing',
            tel: '123-456-789'
        });

        var request = window.navigator.mozContacts.save(contact);

        console.log(request)
        //window.navigator.mozContacts.save(testContact);

        request.onerror = function onerror() {
            console.error('Error saving contact', request.error.name);
        }

        request.onsuccess = function onerror() {
            console.error('Success saving contact', request);
        }

        return request;

    }
};