# [![Build Status](https://travis-ci.org/ntalekt/homeassistant.svg?branch=master)](https://travis-ci.org/ntalekt/homeassistant) Home Assistant Config by ntalekt
This is my [Home Assistant](https://home-assistant.io) configuration which is running on a [Raspberry PI 3 ](https://www.amazon.com/gp/product/B01CD5VC92/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01CD5VC92&linkCode=as2&tag=ntalekt-20&linkId=85008d89d44170ee683cbe85480e5522) running [Hassbian](https://home-assistant.io/docs/installation/hassbian/installation/).

Home Assistant Version: 0.60

## Platform
* [Raspberry PI 3 Model B](https://www.amazon.com/gp/product/B01CD5VC92/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01CD5VC92&linkCode=as2&tag=ntalekt-20&linkId=85008d89d44170ee683cbe85480e5522)
* [SanDisk Ultra 32GB microSDHC](https://www.amazon.com/gp/product/B010Q57T02/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B010Q57T02&linkCode=as2&tag=ntalekt-20&linkId=1f3a281d1767ccf9e81b1eecfb3dc17a)
* [Aeotec Z-Stick Gen5](https://www.amazon.com/gp/product/B00X0AWA6E/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00X0AWA6E&linkCode=as2&tag=ntalekt-20&linkId=ffe37e67106ed75d94683035242bfdc4)
* [NGNIX proxy](https://home-assistant.io/docs/ecosystem/nginx/)
* SSL via [SSLs](https://www.ssls.com/)

## Devices
#### Climate
* [Nest Thermostat](https://www.amazon.com/gp/product/B0131RG6VK/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0131RG6VK&linkCode=as2&tag=ntalekt-20&linkId=e0db21f4ff5fe08d4d88f64ae040fcc3) x2

#### Lighting
* [Hue Hub](https://www.amazon.com/gp/product/B014H2P42K/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B014H2P42K&linkCode=as2&tag=ntalekt-20&linkId=f7c4c6761bc4d3ee0ec55b55dac43419)
* [Hue White Bulb](https://www.amazon.com/gp/product/B073SSK6P8/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B073SSK6P8&linkCode=as2&tag=ntalekt-20&linkId=e23e56d9f8e7207899d06d1e65d1a44a) x4
* [Yeelight WIFI RGB Strip](https://www.amazon.com/gp/product/B01LRT0B56/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&linkCode=as2&tag=ntalekt-20&linkId=f494661c2bfcea4e57c2ee133a4b4caf) x2
* [GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt-20&linkId=28f9845f77c4f9b01c7ad84871a799ab) x3

#### Sensor / Switch
* [Ecolink Z-wave Plus Garage Door Tilt Sensor](https://www.amazon.com/gp/product/B01MRZB0NT/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MRZB0NT&linkCode=as2&tag=ntalekt-20&linkId=ba67bb773710bc24f062775d66fe51b1)
* [BRUH Automation Multisensor](https://github.com/bruhautomation/ESP-MQTT-JSON-Multisensor)
* [Xiaomi Mi Smart Gateway](https://www.gearbest.com/living-appliances/pp_344667.html)
* [Xiaomi Aqara Temperature Humidity Sensor](https://www.gearbest.com/access-control/pp_626702.html) x5
* [Xiaomi Aqara Window Door Sensor](https://www.gearbest.com/access-control/pp_626703.html)
* [Xiaomi Aqara Smart Wireless Switch](https://www.gearbest.com/access-control/pp_626695.html) x2

#### Camera
* [Amcrest IPM-HX1W Camera](https://www.amazon.com/gp/product/B01LZHOILC/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LZHOILC&linkCode=as2&tag=ntalekt-20&linkId=fd29fa84ba58e8747400ea53e05b8459) x4
* [Hikvision DS-2CD2032-I Camera](https://www.amazon.com/gp/product/B00G7GMEOG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00G7GMEOG&linkCode=as2&tag=ntalekt-20&linkId=199e0a6b51f0f83c21855d62219693c0)
* [Ring Pro Doorbell](https://www.amazon.com/gp/product/B01DM6BDA4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DM6BDA4&linkCode=as2&tag=ntalekt-20&linkId=100ed966ea93c748bf857696167a167c)

#### Media
* [Amazon Echo Dot](https://www.amazon.com/gp/product/B015TJD0Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015TJD0Y4&linkCode=as2&tag=ntalekt-20&linkId=f75a8b4c616563e31e98c9cefd43d032) x2 (via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/))
* [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK98/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK98&linkCode=as2&tag=ntalekt-20&linkId=35105866ec0a7f4c67dd1abea7958f5a) x3
* [Sonos One](https://www.amazon.com/All-new-Sonos-One-Controlled-Speaker/dp/B074XN1LH3/ref=sr_1_4?s=aht&ie=UTF8&qid=1514905485&sr=1-4&keywords=sonos%2Bone&th=1)
* [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt-20&linkId=a3f1b5dc6cded9429966fb2cbe90ecf0) x2
* [NVIDIA SHIELD TV](https://www.amazon.com/gp/product/B01N1NT9Y6/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01N1NT9Y6&linkCode=as2&tag=ntalekt-20&linkId=0c9356d35834fc3cb2fbfcf336ea2d8c)
* [LG 65UH8500 65" TV](https://www.amazon.com/gp/product/B019O5F8CQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B019O5F8CQ&linkCode=as2&tag=ntalekt-20&linkId=8705839f33b90a8d4725c293c464d2e8)

#### Network
* [Netgear Nighthawk X4S Router](https://www.amazon.com/gp/product/B0192911RA/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0192911RA&linkCode=as2&tag=ntalekt-20&linkId=2db37b7e2526db6b90a33fd18b482e14)
* [QNAP TS-251+ NAS](https://www.amazon.com/gp/product/B015VNLEOQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015VNLEOQ&linkCode=as2&tag=ntalekt-20&linkId=c4e26f6ec504a6cf0dbf95fb090a17c4)
* [Synology DS212j NAS](https://www.amazon.com/gp/product/B01BNPT1EG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01BNPT1EG&linkCode=as2&tag=ntalekt-20&linkId=a138afffcf6e9599fd76fe50ab4d0097)
* [Aeotec Z-Stick Gen5](https://www.amazon.com/gp/product/B00X0AWA6E/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00X0AWA6E&linkCode=as2&tag=ntalekt-20&linkId=ffe37e67106ed75d94683035242bfdc4)

#### Location
* [Life360 Location Tracking App](https://www.life360.com/)

## Automations
### Notification Audio
* [TTS](https://home-assistant.io/components/tts.google/) "Good Morning" notification over all [Sonos speakers](https://www.amazon.com/gp/product/B00EWCUK98/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK98&linkCode=as2&tag=ntalekt-20&linkId=35105866ec0a7f4c67dd1abea7958f5a). Includes templated date, birthday countdown, weather, to-do's etc.
* [TTS](https://home-assistant.io/components/tts.google/) "Welcome home _User_" notification over all Sonos speakers.
* [TTS](https://home-assistant.io/components/tts.google/) notification when _User_ arrives at specific [Zones](https://home-assistant.io/components/zone/).
* [TTS](https://home-assistant.io/components/tts.google/) notification when _User_ leaves specific zones which includes travel time home.
* [TTS](https://home-assistant.io/components/tts.google/) notification if the garage door has been open for 30 minutes with no motion in garage.
* [TTS](https://home-assistant.io/components/tts.google/) test notification

### Notification Text
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) notification when new Home Assistant version is available on PyPI.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) notification when [Nest thermostats](https://www.amazon.com/gp/product/B0131RG6VK/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0131RG6VK&linkCode=as2&tag=ntalekt-20&linkId=e0db21f4ff5fe08d4d88f64ae040fcc3) go into Home/Away modes.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) notification when critical network devices go offline.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) notification if the garage door is left open after we left the house.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) notification if the garage door is opened and no one is home.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) notification if the garage door has been open for 30 minutes with no motion in garage.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) notification test.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) when SSL certificate expiration sensor <= 10 days.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) when any battery sensor falls below 20%
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) for a failed login attempt.
* [Pushbullet](https://home-assistant.io/components/notify.pushbullet/) if tracked Gearbest item price drops.

### Notification Visual
* [LG WebOS TV Notification](https://home-assistant.io/components/notify.webostv/) when [Ring Pro Doorbell](https://www.amazon.com/gp/product/B01DM6BDA4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DM6BDA4&linkCode=as2&tag=ntalekt-20&linkId=100ed966ea93c748bf857696167a167c) detects motion or is pressed.

### Lights
* Exterior lights ([GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt-20&linkId=28f9845f77c4f9b01c7ad84871a799ab)) on 5 minutes before sunset.
* Exterior lights ([GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt-20&linkId=28f9845f77c4f9b01c7ad84871a799ab)) off 30 minutes after sunrise.
* Exterior lights ([GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt-20&linkId=28f9845f77c4f9b01c7ad84871a799ab)) dim to 35% at 9:00pm
* Interior Media Center lights ([Yeelight WIFI RGB Strip](https://www.amazon.com/gp/product/B01LRT0B56/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&linkCode=as2&tag=ntalekt-20&linkId=f494661c2bfcea4e57c2ee133a4b4caf)) using [Amazon Echo Dot](https://www.amazon.com/gp/product/B015TJD0Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015TJD0Y4&linkCode=as2&tag=ntalekt-20&linkId=f75a8b4c616563e31e98c9cefd43d032) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Interior loft lights ([Hue White Bulb](https://www.amazon.com/gp/product/B073SSK6P8/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B073SSK6P8&linkCode=as2&tag=ntalekt-20&linkId=e23e56d9f8e7207899d06d1e65d1a44a)) using [Amazon Echo Dot](https://www.amazon.com/gp/product/B015TJD0Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015TJD0Y4&linkCode=as2&tag=ntalekt-20&linkId=f75a8b4c616563e31e98c9cefd43d032) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Holiday interior lighting leveraging [Google Calendar Event](https://home-assistant.io/components/calendar.google/) to define the holiday.
* Holiday interior lighting using [Amazon Echo Dot](https://www.amazon.com/gp/product/B015TJD0Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015TJD0Y4&linkCode=as2&tag=ntalekt-20&linkId=f75a8b4c616563e31e98c9cefd43d032) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* ~~Interior loft lights ([Hue White Bulb](https://www.amazon.com/gp/product/B073SSK6P8/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B073SSK6P8&linkCode=as2&tag=ntalekt-20&linkId=e23e56d9f8e7207899d06d1e65d1a44a)) on at 30% 60 minutes before sunset if home.~~
* ~~Interior loft lights ([Hue White Bulb](https://www.amazon.com/gp/product/B073SSK6P8/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B073SSK6P8&linkCode=as2&tag=ntalekt-20&linkId=e23e56d9f8e7207899d06d1e65d1a44a)) off at 8:10pm.~~
* ~~Interior Media Center lights ([Yeelight WIFI RGB Strip](https://www.amazon.com/gp/product/B01LRT0B56/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&linkCode=as2&tag=ntalekt-20&linkId=f494661c2bfcea4e57c2ee133a4b4caf)) on at sunset.~~
* ~~Interior Media Center lights ([Yeelight WIFI RGB Strip](https://www.amazon.com/gp/product/B01LRT0B56/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&linkCode=as2&tag=ntalekt-20&linkId=f494661c2bfcea4e57c2ee133a4b4caf)) off at 8:00pm.~~
* ~~Interior Media Center lights ([Yeelight WIFI RGB Strip](https://www.amazon.com/gp/product/B01LRT0B56/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&linkCode=as2&tag=ntalekt-20&linkId=f494661c2bfcea4e57c2ee133a4b4caf)) on if motion detected after 8:00pm.~~
* ~~Interior Media Center lights ([Yeelight WIFI RGB Strip](https://www.amazon.com/gp/product/B01LRT0B56/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&linkCode=as2&tag=ntalekt-20&linkId=f494661c2bfcea4e57c2ee133a4b4caf)) off if motion not detected for 5min after 8:00pm.~~


### Doorbell
* Exterior lights to 100% if [Ring Pro Doorbell](https://www.amazon.com/gp/product/B01DM6BDA4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DM6BDA4&linkCode=as2&tag=ntalekt-20&linkId=100ed966ea93c748bf857696167a167c) detects motion or is pressed after 9:00pm.
* Exterior lights back to 35% after 30 minutes after doorbell motion or press.

### Media
* Start [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt-20&linkId=a3f1b5dc6cded9429966fb2cbe90ecf0) activity if user selects from HA UI `input_select`.
* Update `input_select` status if physical [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt-20&linkId=a3f1b5dc6cded9429966fb2cbe90ecf0) remote is used to start activity.
* Start playing music on [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK98/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK98&linkCode=as2&tag=ntalekt-20&linkId=35105866ec0a7f4c67dd1abea7958f5a) speakers if user selects music station from `input_select`.
* Start playing music on [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK98/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK98&linkCode=as2&tag=ntalekt-20&linkId=35105866ec0a7f4c67dd1abea7958f5a) speakers if user starts music station using [Amazon Echo Dot](https://www.amazon.com/gp/product/B015TJD0Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015TJD0Y4&linkCode=as2&tag=ntalekt-20&linkId=f75a8b4c616563e31e98c9cefd43d032) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Start [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt-20&linkId=a3f1b5dc6cded9429966fb2cbe90ecf0) activity using [Amazon Echo Dot](https://www.amazon.com/gp/product/B015TJD0Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015TJD0Y4&linkCode=as2&tag=ntalekt-20&linkId=f75a8b4c616563e31e98c9cefd43d032) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Power off [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt-20&linkId=a3f1b5dc6cded9429966fb2cbe90ecf0) activity using [Amazon Echo Dot](https://www.amazon.com/gp/product/B015TJD0Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015TJD0Y4&linkCode=as2&tag=ntalekt-20&linkId=f75a8b4c616563e31e98c9cefd43d032) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Turn on SleepTime mode if [Xiaomi Aqara Smart Wireless Switch](https://www.gearbest.com/access-control/pp_626695.html) is pressed.

### Sonos
* Reset/Regroup all [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK98/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK98&linkCode=as2&tag=ntalekt-20&linkId=35105866ec0a7f4c67dd1abea7958f5a) speakers at 6:00am every morning.
* Group all Sonos' button.

### Occupancy
* If motion is detected via [BRUH Automation multisensor](https://github.com/bruhautomation/ESP-MQTT-JSON-Multisensor) or [Amcrest  cameras](https://www.amazon.com/gp/product/B01LZHOILC/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LZHOILC&linkCode=as2&tag=ntalekt-20&linkId=fd29fa84ba58e8747400ea53e05b8459) turn on `input_boolean` (used in `binary_sensor` for occupancy tracking).
* If no motion is detected after certain period of time turn off `input_boolean`.

### Sleep time
* Turn off master TV after 30 minutes via [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt-20&linkId=a3f1b5dc6cded9429966fb2cbe90ecf0).

### System
* Run script to collect Cox Internet usage hourly.
* Clean the TTS cache weekly.

### Vacation
* Turn vacation mode on when household is gone for 24 hours.
* Put [Nest Thermostats](https://www.amazon.com/gp/product/B0131RG6VK/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B0131RG6VK&linkCode=as2&tag=ntalekt-20&linkId=e0db21f4ff5fe08d4d88f64ae040fcc3) in away mode when vacation mode active.

## Scripts/Customizations
* Life360 integration via shell mqtt broker found [here](https://community.home-assistant.io/t/life-360-support/1690)
* Home Assistant mysql database size sensor found [here](https://community.home-assistant.io/t/large-homeassistant-database-files/4201/234?u=ntalekt)
* Cox internet usage web parser script found [here](https://community.home-assistant.io/t/cox-communications-internet-usage/28565?u=ntalekt)
* WAN test script found [here](https://community.home-assistant.io/t/wan-test-script-quick-and-dirty/30699)

# Interface
![UI](images/home-screenshot.jpg)
![UI](images/lights-screenshot.jpg)
![UI](images/first-floor-screenshot.jpg)
![UI](images/second-floor-screenshot.jpg)
![UI](images/media-screenshot.jpg)
![UI](images/automation-screenshot.jpg)
![UI](images/sensor-screenshot.jpg)
