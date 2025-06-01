# Astromech

## OS Setup

**Recommended OS:** *Raspberry Pi OS Lite (64-bit)*

You can use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to setup an SD card for this project, just make sure to select your Pi model and the 64-bit Lite OS, or another OS of your prefer.

1. Raspberry Pi OS updates:
    We'll start with updating your Raspberry Pi's firmware:
    ```
    sudo rpi-update
    ```
    After that's complete, make sure to reboot before running the commands below.
    ```
    sudo apt update
    sudo apt upgrade
    ```
2. Install git:
    ```
    sudo apt install git
    ```
3. (TODO: write step 3)
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
