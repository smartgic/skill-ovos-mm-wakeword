[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/mycroft-magicmirror-wakeword-skill/pulls) [![Skill: MIT](https://img.shields.io/badge/ovos-skill-blue)](https://openvoiceos.org) [![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.gg/Vu7Wmd9j)

# <img src="docs/magicmirror.png" card_color="#0000" width="150" height="30" style="vertical-align:bottom"/> MagicMirror² wake word detection

Image and message display on MagicMirror² when Open Voice OS is listening.

## About

[MagicMirror²](https://magicmirror.builders/) is an open source modular smart mirror platform. With a growing list of installable modules, the MagicMirror² allows you to convert your hallway or bathroom mirror into your personal assistant.

This skill interacts with MagicMirror² to let you know if OVOS is listening. When a wake word is detected the an image and message are display on the screen and when the recording is done image and the message disappear.

<img src='docs/screenshot.png' width='450'/>

## Examples

There is no example because there is no voice interaction with Open Voice OS.

## Installation

```shell
$ pip install ovos-magicmirror-wakeword-skill
```

## Configuration

This skill utilizes the `settings.json` file which allows you to configure this skill via `home.mycroft.ai` after a few seconds of having the skill installed you should see something like below in the https://home.mycroft.ai/#/skill location:

<img src='docs/magicmirror-wakeword-config.png' width='450'/>

Fill this out with your appropriate information and hit save.

## MagicMirror configuration

In order to reach the `/ovos` route on your MagicMirror, you need to allow the remote connection for a specific IP address or for a network range.

Please have a look here: https://github.com/smartgic/MMM-ovos-wakeword

## Credits

Smart'Gic

## Category

**IoT**

## Tags

#smartmirror
#magicmirror
#wakeword
#raspberrypi
#smarthome
#picroft
