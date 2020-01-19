# Huawei HG659 API
An API for Huawei HG659 modems allowing you to automatically remove entries from the LAN device list and reboot the modem.

**This was developed to overcome limitations in the Dodo Australia Huawei HG659 modem firmware: V100R001C270B011_Dodo.**
**With this firmware devices may fail to connect once the device list count reaches 32, and deleting devices from the list and rebooting is the only way to reliably address this issue.**

How to use:
- In the python script substitute your router login, password and the WiFI MAC address for the device running the script.
- There is a main function included demonstrating how to use the API.
- You could run this script at a regular interval using Windows Task Scheduler.

Note: This script has only been tested with the aforementioned firmware version.
