<h1 align="center">
  Home Assistant Config by ntalekt
</h1>
<h4 align="center">Be sure to :star: my repo so you can keep up to date on the progress!</h4>
<div align="center">
  <h4>
    <a href="https://github.com/ntalekt/homeassistant/stargazers"><img src="https://img.shields.io/github/stars/ntalekt/homeassistant.svg"/></a>
    <a href="https://github.com/ntalekt/homeassistant/commits/dev"><img src="https://img.shields.io/github/last-commit/ntalekt/homeassistant.svg"/></a>
  </h4>
</div>
This is my <a href="https://home-assistant.io">Home Assistant</a> configuration which is running on Docker. When starting with home automation I found many well documented configurations and drew inspiration from them in order to achieve my automation goals. I wanted to share my success with the community and hopefully help others on their journey.

#### Platform
* Hardware
  * [HP Z620 - E5-2650 8C, 64GB ECC]
  * [QNAP TS-251+](https://www.qnap.com/en-us/product/ts-251+)
  * [Aeotec Z-Stick Gen5](https://www.amazon.com/gp/product/B00X0AWA6E/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00X0AWA6E&linkCode=as2&tag=ntalekt0c-20&linkId=04f4c7bf8438a9dee6e4e2ad273405d0)
* Software
  * [homeassistant/home-assistant](https://hub.docker.com/r/homeassistant/home-assistant)
    * Home Assistant Version: 2021.2.3
  * [Docker v19.03.12](https://github.com/docker/docker-ce/releases)
  * [Traefik v2.2.1 proxy](https://www.smarthomebeginner.com/traefik-2-docker-tutorial/)
  * SSL via [Let's Encrypt](https://letsencrypt.org/)
  
# Interface
![UI](images/home-lovelace.jpg)
![UI](images/climate.jpg)
![UI](images/system-network.jpg)
![UI](images/sensors.jpg)
![UI](images/automation.jpg)

## Devices

#### Lighting
* [Yeelight WIFI RGB Strip](https://smile.amazon.com/gp/product/B01LRT0B56/ref=smi_www_rco2_go_smi_4368549507?_encoding=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&ie=UTF8&linkCode=as2&linkId=34a9570cd0c747f448092913ac2dae60&tag=ntalekt0c-20) x2
* [GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt0c-20&linkId=0dfbcad4a9df3b81570623f0e23b562a) x3
* [LE LampUX RGB Lamp](https://smile.amazon.com/gp/product/B07Q8SMG8R/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1)
* [Goldwin Wifi Controller](https://smile.amazon.com/gp/product/B07JB5N3Y7/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)

#### Climate
* [Trane XL824](https://smile.amazon.com/Trane-Programmable-Comfort-Control-Thermostat/dp/B085W87WY3/ref=sr_1_1?dchild=1&keywords=xl824&qid=1595374599&s=hi&sr=1-1) x2

#### Outlets / Switchs
* [Xiaomi Aqara Smart Wireless Switch](https://www.aqara.com/us/wireless_mini_switch.html) x4
* [Wemo Mini Smart Plug](https://www.amazon.com/gp/product/B01NBI0A6R/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01NBI0A6R&linkCode=as2&tag=ntalekt0c-20&linkId=b8975bef5cfef090873209417be305fa)
* [Wemo Insight Smart Plug](https://www.amazon.com/gp/product/B01DBXNYCS/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DBXNYCS&linkCode=as2&tag=ntalekt0c-20&linkId=934f0720129cf096876ab8b14a26bbbb)
* [Tuya Compatible Smart Plug](https://smile.amazon.com/dp/B07FVST9YN/?coliid=I2R80H7TIDHPO5&colid=3LNUCWJAWZGG4&psc=1&ref_=lv_ov_lig_dp_it)

#### Sensors
* [Ecolink Z-wave Plus Garage Door Tilt Sensor](https://www.amazon.com/gp/product/B01MRZB0NT/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MRZB0NT&linkCode=as2&tag=ntalekt0c-20&linkId=ba6f517d4382e6a23be0479e15d3ce2f)
* [Xiaomi Mi Smart Gateway](https://www.aqara.com/us/smart_home_hub.html)
* [Xiaomi Aqara Motion Sensor](https://www.aqara.com/us/motion_sensor.html) x2
* [Xiaomi Aqara Temperature Humidity Sensor](https://www.aqara.com/us/temperature_humidity_sensor.html) x5
* [Xiaomi Aqara Window Door Sensor](https://www.aqara.com/us/door_and_window_sensor.html)

#### Camera
* [Amcrest IP3M-943W Camera](https://www.amazon.com/gp/product/B01I01Z1M2/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01I01Z1M2&linkCode=as2&tag=ntalekt0c-20&linkId=2ef3afe981c97da79ba37bf3815f7347)
* [Amcrest IPM-HX1W Camera](https://www.amazon.com/gp/product/B077DPWQCV/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B077DPWQCV&linkCode=as2&tag=ntalekt0c-20&linkId=ac62ed590e7bb7ab3e4aca12348c1db1) x4
* [Hikvision DS-2CD2032-I Camera](https://www.amazon.com/gp/product/B00G7GMEOG/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00G7GMEOG&linkCode=as2&tag=ntalekt0c-20&linkId=6033949532ab30894bc0ef3dfb3e4757)
* [Ring Pro Doorbell](https://www.amazon.com/gp/product/B01DM6BDA4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DM6BDA4&linkCode=as2&tag=ntalekt0c-20&linkId=5faec88af320aeb157fbb45fa954efc3)

#### Media
* [Amazon Echo Dot](https://www.amazon.com/gp/product/B01DFKC2SO/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DFKC2SO&linkCode=as2&tag=ntalekt0c-20&linkId=bb902528d5689ae4e1163dd31b7c646d) x2 (via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/))
* [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK1Q/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK1Q&linkCode=as2&tag=ntalekt0c-20&linkId=b90ba9470832833ea363027daabf948a) x3
* [Sonos One](https://www.amazon.com/gp/product/B074XLMYY5/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B074XLMYY5&linkCode=as2&tag=ntalekt0c-20&linkId=7be4e37d04615af0d61054e6d5378aa7)
* [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt0c-20&linkId=ef1edfe63776ff2e3b5b4e7fdf8e3488) x2
* [NVIDIA SHIELD TV](https://www.amazon.com/gp/product/B01N1NT9Y6/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01N1NT9Y6&linkCode=as2&tag=ntalekt0c-20&linkId=d90fc7313c3e4e91d21098784afceef1)
* [LG 65UH8500 65" TV](https://www.amazon.com/gp/product/B01N4TQ7O4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01N4TQ7O4&linkCode=as2&tag=ntalekt0c-20&linkId=8f7ccb7cacee84993798af9970cd6bb8)

#### Irrigation
* [Rain Bird ST8O-2.0](https://www.rainbird.com/products/st8-20-wifi-smart-irrigation-timers)

#### Network
* [Ubiquiti Unifi Security Gateway (USG)](https://smile.amazon.com/Ubiquiti-Unifi-Security-Gateway-USG/dp/B00LV8YZLK/ref=sr_1_1?s=electronics&ie=UTF8&qid=1551113819&sr=1-1)
* [Ubiquiti UniFi Switch 8 60W (US-8-60W)](https://smile.amazon.com/Ubiquiti-UniFi-Switch-60W-US-8-60W/dp/B01MU3WUX1/ref=sr_1_1?s=electronics&ie=UTF8&qid=1551113861&sr=1-1)
* [Ubiquiti UniFi Access Point (UAP-AC-PRO-US)](https://smile.amazon.com/Ubiquiti-Networks-802-11ac-Dual-Radio-UAP-AC-PRO-US/dp/B015PRO512/ref=pd_bxgy_147_3/147-7827003-3388156?_encoding=UTF8&pd_rd_i=B015PRO512&pd_rd_r=78e61fca-391e-11e9-8361-31a05a5f3960&pd_rd_w=EtNic&pd_rd_wg=9CHgg&pf_rd_p=6725dbd6-9917-451d-beba-16af7874e407&pf_rd_r=PWC60BR9T4G7454SPZJM&psc=1&refRID=PWC60BR9T4G7454SPZJM) x2

#### Other Hardware
* [QNAP TS-251+ NAS](https://www.amazon.com/gp/product/B015VNLEOQ/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B015VNLEOQ&linkCode=as2&tag=ntalekt0c-20&linkId=1419a45442b188e9223b9afd7da40d5c)
* [Aeotec Z-Stick Gen5](https://www.amazon.com/gp/product/B00X0AWA6E/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00X0AWA6E&linkCode=as2&tag=ntalekt0c-20&linkId=04f4c7bf8438a9dee6e4e2ad273405d0)
* [APC APC BX1500M] (https://www.amazon.com/APC-Battery-Protector-BackUPS-BX1500M/dp/B06VY6FXMM)

#### Software
* [Life360 Location Tracking App](https://www.life360.com/)
* [Pi-hole] (https://pi-hole.net/)

## Example Automations
### Notification Audio
* [TTS](https://home-assistant.io/components/tts.google/) notification when _User_ arrives at specific [Zones](https://home-assistant.io/components/zone/).
* [TTS](https://home-assistant.io/components/tts.google/) notification when _User_ leaves specific zones which includes travel time home.
* [TTS](https://home-assistant.io/components/tts.google/) notification if the garage door has been open for 30 minutes with no motion in garage.
* [TTS](https://home-assistant.io/components/tts.google/) school bell notification (if remote schooling mode enabled)
* [TTS](https://home-assistant.io/components/tts.google/) test notification

### Notification Text
* [Slack](https://www.home-assistant.io/integrations/slack) notification when new Home Assistant version is available on PyPI.
* [Slack](https://www.home-assistant.io/integrations/slack) notification when critical network devices go offline.
* [Slack](https://www.home-assistant.io/integrations/slack) notification if the garage door is left open after we left the house.
* [Slack](https://www.home-assistant.io/integrations/slack) notification if the garage door is opened and no one is home.
* [Slack](https://www.home-assistant.io/integrations/slack) notification if the garage door has been open for 30 minutes with no motion in garage.
* [Slack](https://www.home-assistant.io/integrations/slack) notification test.
* [Slack](https://www.home-assistant.io/integrations/slack) when any battery sensor falls below 20%
* [Slack](https://www.home-assistant.io/integrations/slack) for a failed login attempt.
* [Slack](https://www.home-assistant.io/integrations/slack) if new network device is detected.

### Lights
* Exterior lights ([GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt0c-20&linkId=0dfbcad4a9df3b81570623f0e23b562a)) on 5 minutes before sunset.
* Exterior lights ([GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt0c-20&linkId=0dfbcad4a9df3b81570623f0e23b562a)) off 30 minutes after sunrise.
* Exterior lights ([GE Z-Wave Plus Dimmer 14294](https://www.amazon.com/gp/product/B01MUCZA1C/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01MUCZA1C&linkCode=as2&tag=ntalekt0c-20&linkId=0dfbcad4a9df3b81570623f0e23b562a)) dim to 35% at 9:00pm
* Interior Media Center lights ([Yeelight WIFI RGB Strip](https://www.amazon.com/gp/product/B01LRT0B56/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01LRT0B56&linkCode=as2&tag=ntalekt0c-20&linkId=34a9570cd0c747f448092913ac2dae60)) using [Amazon Echo Dot](https://www.amazon.com/gp/product/B01DFKC2SO/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DFKC2SO&linkCode=as2&tag=ntalekt0c-20&linkId=bb902528d5689ae4e1163dd31b7c646d) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).

### Doorbell
* Exterior lights to 100% if [Ring Pro Doorbell](https://www.amazon.com/gp/product/B01DM6BDA4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DM6BDA4&linkCode=as2&tag=ntalekt0c-20&linkId=5faec88af320aeb157fbb45fa954efc3) detects motion or is pressed after 9:00pm.
* Exterior lights back to 35% after 30 minutes after doorbell motion or press.

### Media
* Start [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt0c-20&linkId=ef1edfe63776ff2e3b5b4e7fdf8e3488) activity if user selects from HA UI `input_select`.
* Update `input_select` status if physical [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt0c-20&linkId=ef1edfe63776ff2e3b5b4e7fdf8e3488) remote is used to start activity.
* Start playing music on [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK1Q/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK1Q&linkCode=as2&tag=ntalekt0c-20&linkId=b90ba9470832833ea363027daabf948a) speakers if user selects music station from `input_select`.
* Start playing music on [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK1Q/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK1Q&linkCode=as2&tag=ntalekt0c-20&linkId=b90ba9470832833ea363027daabf948a) speakers if user starts music station using [Amazon Echo Dot](https://www.amazon.com/gp/product/B01DFKC2SO/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DFKC2SO&linkCode=as2&tag=ntalekt0c-20&linkId=bb902528d5689ae4e1163dd31b7c646d) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Start [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt0c-20&linkId=ef1edfe63776ff2e3b5b4e7fdf8e3488) activity using [Amazon Echo Dot](https://www.amazon.com/gp/product/B01DFKC2SO/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DFKC2SO&linkCode=as2&tag=ntalekt0c-20&linkId=bb902528d5689ae4e1163dd31b7c646d) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Power off [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt0c-20&linkId=ef1edfe63776ff2e3b5b4e7fdf8e3488) activity using [Amazon Echo Dot](https://www.amazon.com/gp/product/B01DFKC2SO/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DFKC2SO&linkCode=as2&tag=ntalekt0c-20&linkId=bb902528d5689ae4e1163dd31b7c646d) via [Emulated Hue Bridge](https://home-assistant.io/components/emulated_hue/).
* Turn on SleepTime mode if [Xiaomi Aqara Smart Wireless Switch](https://www.gearbest.com/access-control/pp_626695.html) is pressed.
* Pause [Deluge](https://home-assistant.io/components/switch.deluge/) if internet data usage > 90%.

### Sonos
* Reset/Regroup all [Sonos PLAY:1](https://www.amazon.com/gp/product/B00EWCUK1Q/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00EWCUK1Q&linkCode=as2&tag=ntalekt0c-20&linkId=b90ba9470832833ea363027daabf948a) speakers at 6:00am every morning.
* Group all Sonos' button.

### Occupancy
* If motion is detected via [BRUH Automation multisensor](https://github.com/bruhautomation/ESP-MQTT-JSON-Multisensor) or [Amcrest  cameras](https://www.amazon.com/gp/product/B077DPWQCV/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B077DPWQCV&linkCode=as2&tag=ntalekt0c-20&linkId=ac62ed590e7bb7ab3e4aca12348c1db1) turn on `input_boolean` (used in `binary_sensor` for occupancy tracking).
* If no motion is detected after certain period of time turn off `input_boolean`.

### Sleep time
* Turn off master TV after 30 minutes via [Harmony Hub](https://www.amazon.com/gp/product/B00BQ5RYI4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B00BQ5RYI4&linkCode=as2&tag=ntalekt0c-20&linkId=ef1edfe63776ff2e3b5b4e7fdf8e3488).

### System
* Run script to collect Cox Internet usage hourly.
* Clean the TTS cache weekly.

### Vacation/Climate
* Turn vacation mode on when household is gone for 24 hours.
* Toggle office fan on/off based on occupancy using * [Wemo Insight Smart Plug](https://www.amazon.com/gp/product/B01DBXNYCS/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B01DBXNYCS&linkCode=as2&tag=ntalekt0c-20&linkId=934f0720129cf096876ab8b14a26bbbb).
