# Astromech

## Software Setup

**Recommended OS:** *Raspberry Pi OS Lite (64-bit)*

You can use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to setup an SD card for this project, just make sure to select your Pi model and the 64-bit Lite OS, or another OS of your prefer.

### OS Setup

1. **Raspberry Pi OS updates**  
    Start with pulling new packages and updating the ones you have:
    ```
    sudo apt update
    sudo apt upgrade
    ```
    (Optional) After that's done, run `rpi-update` to grab any firmware updates for your Pi and `sudo reboot` to reboot and apply them.
2. **Install dependencies:**  
    We'll be depending on several packages for front-end stuff, I/O, or version management, you can install separately (using `sudo apt install <package-name>`) or together using this single-line command:
    ```
    sudo apt install git python3-flask python3-picamera2
    ```
### Hotspot setup:
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


### Driver installation

1. *(optional)* **Camera verification**  
    Verify your camera is connected to your Pi using:
    ```
    rpicam-hello --list-cameras
    ```
    You should see info on your camera module printed out:
    ```
    Available cameras
    -----------------
    0 : ov5647 [2592x1944 10-bit GBRG] (/base/soc/i2c0mux/i2c@1/ov5647@36)
        Modes: 'SGBRG10_CSI2P' : 640x480 [58.92 fps - (16, 0)/2560x1920 crop]
                                1296x972 [46.34 fps - (0, 0)/2592x1944 crop]
                                1920x1080 [32.81 fps - (348, 434)/1928x1080 crop]
                                2592x1944 [15.63 fps - (0, 0)/2592x1944 crop]
    ```

4. Download & install gStreamer (instructions excerpt from [here](https://platypus-boats.readthedocs.io/en/latest/source/rpi/video/video-streaming-gstreamer.html#getting-gstreamer)):
    ```
    sudo add-apt-repository ppa:gstreamer-developers/ppa
    sudo apt-get update
    sudo apt-get install gstreamer1.0*
    ```

3. Install WM8960 driver (instrutions excerpt from [here](https://github.com/waveshareteam/WM8960-Audio-HAT))  
  I cloned this repo into a new folder, but where you place it is up to you.
    ```
    git clone https://github.com/waveshare/WM8960-Audio-HAT
    cd WM8960-Audio-HAT
    sudo ./install.sh
    sudo reboot
    ```
    Running `install.sh` should also install `i2c-tools`, which we can use to verify the PCA9685's connection:
    ```
    i2cdetect -y 1
    ```
    Running the i2c detection command above should show all connected I2C devices and their addresses. The PCA9685 should show up as 0x40 (default) or 0x41, etc varying depending on if the address was changed.
  4. Install PCA9685 driver for Pi (instructions excerpt from [here](https://github.com/barulicm/PiPCA9685/blob/main/README.md))
      - Clone the repo
      ```
      git clone https://github.com/barulicm/PiPCA9685.git
      ```
      - Install the driver's dependencies
      ```
      cd PiPCA9685
      xargs -a apt_dependencies.txt sudo apt-get install -y
      ```
      - Build and install the library
      ```
      sudo cmake --workflow --preset install
      ```
