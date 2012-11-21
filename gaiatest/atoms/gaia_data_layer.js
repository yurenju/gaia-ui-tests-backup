/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

var GaiaDataLayer = {

    insertContact: function(cdata){
        contact = new mozContact();
        contact.init(cdata);
        var request = window.navigator.mozContacts.save(contact);

        request.onerror = function onerror() {
            console.log('Error saving contact', request.error.name);
        }

        request.onsuccess = function onsuccess() {
            console.log('Success saving contact', request);
        }
        return request;
    },

    findAndRemoveContact: function(cdata){
        var options = {filterBy: ["familyName"],
            filterOp: "contains",
            filterValue: cdata['familyName']};

        contact = window.navigator.mozContacts.find(options);

        contact.onerror = function onerror() {
            console.log('Could not find contact', contact.error.name);
        }

        contact.onsuccess = function onsuccess() {
            console.log('Success finding contact', contact);
            if(contact.result.length > 0){
                return window.navigator.mozContacts.remove(contact.result[0]);
            }
        }
    },

    setVolume: function(vdata){
        lock = window.navigator.mozSettings.createLock();
        volume = lock.set({"audio.volume.master":vdata});
        lock.clear();
        volume.onerror = function onerror(){
            console.log('volume set failed', volume.error.name);
        }
    },

    enableWiFi: function(){
        lock = window.navigator.mozSettings.createLock();
        wifiOn = lock.set({"wifi.enabled": true});
        wifiOn.onsuccess = function(){
            console.log('WiFi ON');
            return true;
        }

        wifiOn.onerror = function(){
            console.log('WiFi On failed', wifiOn.error.name);
            return false;
        }
    },

    disableWiFi: function(){
        lock = window.navigator.mozSettings.createLock();
        wifiOn = lock.set({"wifi.enabled": false});
        wifiOn.onsuccess = function(){
            console.log('WiFi OFF');
            return true;
        }

        wifiOn.onerror = function(){
            console.log('WiFi OFF failed', wifiOn.error.name);
            return false;
        }
    },

    connectToWiFi: function(ssid){
        var manager = window.navigator.mozWifiManager;
        var req = manager.getNetworks();

        req.onsuccess = function onScanSuccess() {
            var allNetworks = req.result;
            var preferredNetwork = allNetworks[ssid];

            connect = manager.associate(preferredNetwork);
            connect.onerror = function (){
                console.log('Connection to '+ ssid + ' failed', connect.error.name);
                return false;
            }

            connect.onsuccess = function() {
                console.log('Connected to ' + ssid);
                return true;
            }
        }

        req.onerror = function(){
            console.log('Could not get the available network list', req.error.name);
            return false;
        }

    },

    forgetWiFi: function(ssid){
        var manager = window.navigator.mozWifiManager;
        var req = manager.getKnownNetworks();

        req.onsuccess = function () {
            var allNetworks = req.result;
            var preferredNetwork = allNetworks[ssid];

            forget = manager.forget(preferredNetwork);
            forget.onerror = function (){
                console.log('Forgetting network' + ssid + ' failed', forget.error.name);
                return false;
            }

            forget.onsuccess = function() {
                console.log('Forgotten network ' + ssid);
                return true;
            }
        }

        req.onerror = function(){
            console.log('Could not get the known network list', req.error.name);
            return false;
        }

    }
};
