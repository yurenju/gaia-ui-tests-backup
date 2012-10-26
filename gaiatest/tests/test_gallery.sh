#!/bin/bash
set -x

function proc {
  adb wait-for-device
  adb shell b2g-ps | grep Homescreen
  result=$?
  while [ "$result" -eq "1"  ]; do
    sleep 10
    adb shell b2g-ps | grep Homescreen
    result=$?
  done

  adb forward tcp:2828 tcp:2828
  gaiatest --address localhost:2828 test_gallery.py
  sleep 3
  java -jar /home/yurenju/apps/screenshot.jar -d screenshots/$1.png
  adb reboot
}


for i in {1..10}
do
  proc $i
done