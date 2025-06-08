# Home Assistant CCM15 Integration

The CCM15 integration allows you to integrate [Midea CCM15](https://mbt.midea.com/hvac-goods/midea-products-category/vrfs/vrf-controller/central-controller-ccm-15) devices in Home Assistant.

> Home Assistant has release [official ccm15 integration](https://www.home-assistant.io/integrations/ccm15/), please try official integration first!
> But if you found issues while using the official integration, feel free to use this custom component.

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![Coverage][coverage-shield]][coverage]
![GitHub all releases][download-all]
![GitHub release (latest by SemVer)][download-latest]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

## Installation

### Installation Methods
#### HACS
Click the following link to add to your Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=daxingplay&repository=home-assistant-midea-ccm15&category=integration)

#### Manual
Copy `custom_components/ccm15` into your Home Assistant `config` directory.

### Post installation steps
- Restart HA
- Search for this integration in `Settings -> Devices & Services`
- Click `Add integration` and search for `CCM15`
- Click `Configure` in CCM15 integration to start config flow
- Enter your host and port for ccm15 controller
- If connects successfully, the air conditioner devices will be automatically showed up in the device and entity list
- All done

## Contributions are welcome!
If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

Component built with integration_blueprint.

***

[buymecoffee]: https://www.buymeacoffee.com/daxingplay
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square
[commits-shield]: https://img.shields.io/github/commit-activity/y/daxingplay/home-assistant-midea-ccm15.svg?style=flat-square
[commits]: https://github.com/daxingplay/home-assistant-midea-ccm15/commits/master
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square
[coverage-shield]: https://img.shields.io/coverallsCoverage/github/daxingplay/home-assistant-midea-ccm15?style=flat-square
[coverage]: https://coveralls.io/github/daxingplay/home-assistant-midea-ccm15?branch=master
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=flat-square
[forum]: https://github.com/daxingplay/home-assistant-midea-ccm15/issues
[license]: https://github.com/daxingplay/home-assistant-midea-ccm15/blob/master/LICENSE
[license-shield]: https://img.shields.io/github/license/daxingplay/home-assistant-midea-ccm15.svg?style=flat-square
[maintenance-shield]: https://img.shields.io/badge/maintainer-daxingplay-blue.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/release/daxingplay/home-assistant-midea-ccm15.svg?style=flat-square
[releases]: https://github.com/daxingplay/home-assistant-midea-ccm15/releases
[user_profile]: https://github.com/daxingplay
[download-all]: https://img.shields.io/github/downloads/daxingplay/home-assistant-midea-ccm15/total?style=flat-square
[download-latest]: https://img.shields.io/github/downloads/daxingplay/home-assistant-midea-ccm15/latest/total?style=flat-square