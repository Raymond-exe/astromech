# Astromech

## OS Setup
1. Raspberry Pi OS updates:
    ```
    sudo apt update
    sudo apt upgrade
    ```
2. Install git:
    ```
    sudo apt install git
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
