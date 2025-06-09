# Hotspot setup

This guide is intended to be followed **without needing an external Wi-Fi dongle**. As long as your Raspberry Pi model has on-board Wi-Fi hardware, you should be able to use this guide to create a hotspot *without* any extra hardware.

I've combined **several** guides on how to create a hotspot with the current Raspberry Pi OS Lite release, bookworm. These guides are:
- [How can I create a Wireless Access Point while connected to wireless?](https://forums.raspberrypi.com/viewtopic.php?t=354591&sid=1b6020fedecc19f4e9029d7f0c3f6169) on the Raspberry Pi Forums, referenced for how to create the `uap0` network interface.
- [Create a Wifi Hotspot on Raspberry Pi with NetworkManager](https://gist.github.com/max-pfeiffer/9e8e76d190698cc8381b75399c1ded1d) by [Max Pfeiffer](https://gist.github.com/max-pfeiffer) on GitHub Gists. We'll be using Max's guide for the `nmcli` command syntax.
- Lastly, [Host a Wi-Fi hotspot with a Raspberry Pi](https://www.raspberrypi.com/tutorials/host-a-hotel-wifi-hotspot/), an official Raspberry Pi guide which uses similar syntax to Max's guide, but excludes the connection name option (which I personally think is handy) but includes a basic network portal.  

Please note, **if you new to interacting with a command-line interface** or otherwise don't feel comfortable with it yet, you may want to consider purchasing a Wi-Fi dongle and following the [official Raspberry Pi guide](https://www.raspberrypi.com/tutorials/host-a-hotel-wifi-hotspot/) on creating a hotspot. You'll more or less end up in a similar place after that.

1. We'll start by writing a service to create uap0 interface on boot. Create/edit the file: 
    ```
    sudo nano /etc/systemd/system/uap0.service
    ```
    And paste the following content.
    ```
    [Unit]
    Description=Create uap0 interface
    After=sys-subsystem-net-devices-wlan0.device

    [Service]
    Type=oneshot
    RemainAfterExit=true
    ExecStart=/sbin/iw phy phy0 interface add uap0 type __ap
    ExecStartPost=/usr/bin/ip link set dev uap0 address 00:11:22:33:44:55
    ExecStartPost=/sbin/ifconfig uap0 up
    ExecStop=/sbin/iw dev uap0 del

    [Install]
    WantedBy=multi-user.target
    ```
    > __Replace `00:11:22:33:44:55` with the Pi's MAC address for your access point.__  
    > You can run `ifconfig | grep ether` to find your Pi's MAC address.

    Press ^X to close and **save** the file.

2. Reload daemon so it can read info about this service, and enable service so it run on boot:
    ```
    sudo systemctl daemon-reload
    sudo systemctl start uap0.service
    sudo systemctl enable uap0.service
    ```
    You can now verify you have `uap0` as a network interface by running `ip addr list`.

3. With uap0 initialized, we can use the following command to create a hotspot through NetworkManager:
    ```
    sudo nmcli connection add con-name uap0-hotspot type wifi ifname uap0 wifi.mode ap wifi.ssid <SSID> wifi-sec.key-mgmt wpa-psk wifi-sec.psk <PASSWORD> ipv4.method shared
    ```
    > Set \<SSID> to whatever you'd like the network name to be.  
    > Set \<PASSWORD> to something secure, we wouldn't want others gaining control of the droid!

    Now, running `nmcli con` should show your hotspot live as `uap0-hotspot`. You can change this connection name if you want, but it won't be visible to anyone but you and is only used internally.

4. Modify the connection to always run after rebooting:
    ```
    sudo nmcli connection modify uap0-hotspot connection.autoconnect yes connection.autoconnect-priority 100
    ```
    > If you changed the connection name to something other than `uap0-hotspot`, you'll need to use that name instead.

You should now be able to connect to your Raspberry Pi's hotspot. Any time the Pi reboots, the hotspot network should automatically appear again. If the Pi is already connected to *another* network with internet access, your devices connected to the Pi's hotspot should also be able to access the internet. You can follow [official Raspberry Pi guide](https://www.raspberrypi.com/tutorials/host-a-hotel-wifi-hotspot/) to also create a Wi-Fi config page if you'd like, allowing you to change the parent network while being connected to the hotspot's network.

## Next
Continue on to the [Software setup guide](./SOFTWARE.md).
