/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

var GaiaDataLayer = {

    insertContact: function(cdata){
        var contact = new mozContact();
        contact.init(cdata);
        var req = window.navigator.mozContacts.save(contact);

        //window.navigator.mozContacts.save(testContact);
        return req;
    }

};