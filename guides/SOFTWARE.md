# Software setup
> You should finish the [hotspot setup guide]() before following this one.

## Driver installation
These steps I performed inside a new `drivers` directory I made in my home folder, but however you'd like to organize these is up to you, since they'll really only be used for installation (and if you run into trouble, uninstallation).

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

2. Install PCA9685 driver for Pi (instructions excerpt from [here](https://github.com/barulicm/PiPCA9685/blob/main/README.md))
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

3. Install WM8960 driver (instrutions excerpt from [here](https://github.com/ubopod/WM8960-Audio-HAT))  
    > Note: *This is **not** the official driver from the Waveshare Team*, but a set of updated drivers for kernel 6.12 compatibility. The original driver repo is available [here](https://github.com/waveshareteam/WM8960-Audio-HAT/).

    First, make sure you have the Linux Kernel Headers for your kernel version:
    ```
    sudo apt install linux-headers-$(uname -r)
    ```
    Then, follow the install instructions listed on the git README:
    ```
    git clone https://github.com/ubopod/WM8960-Audio-HAT
    cd WM8960-Audio-HAT
    sudo ./install.sh
    sudo reboot
    ```
    After that, ensure `wm8960soundcard` shows up when running `aplay -l` and `arecord -l`.  
    To test the microphone and speaker, you can run the following command:
    ```
    arecord -f cd -Dhw:0 | aplay -Dhw:0
    ```
    > Make sure to use the WM8960's card number found in `aplay -l` and `arecord -l` for each `-Dhw` argument above. Example: `-Dhw:99` if the WM8960 is, for some reason, `card 99: <...>`.

    Running `install.sh` should also install `i2c-tools`, which we can use to verify the PCA9685 servo driver board's connection:
    ```
    i2cdetect -y 1
    ```
    Running the i2c detection command above should show all connected I2C devices and their addresses. The PCA9685 should show up as 0x40 (default) or 0x41, etc varying depending on if the address was changed.


## Codebase and auto-updates
> **Important:** if you plan to make software customizations or other changes you want to keep, *make sure to fork this repository* before continuing. The `run.sh` file executed each time the droid boots will pull changes made to **this repository**, unless you make your own fork instead.

1. Start by cloning this repository into your home folder:
    ```
    git clone https://github.com/Raymond-exe/astromech.git
    ```
    > If you clone the repository into somewhere *aside* from your home folder, make sure to remember the filepath for later use in this guide.
2. Add `run.sh` to run on boot. You can do this via crontab by running `sudo crontab -e` and pasting the following text:
    ```
    @reboot bash /home/YOUR_USERNAME/astromech/run.sh
    ```
3. 