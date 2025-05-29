# Astromech

## OS Setup
- Raspberry Pi OS updates:
    ```
    sudo apt update
    sudo apt upgrade
    ```
- Install git:
    ```
    sudo apt install git
    ```
- Install WM8960 driver (instrutions excerpt from [here](https://github.com/waveshareteam/WM8960-Audio-HAT))  
  I cloned this repo into a new folder, 
  ```
  git clone https://github.com/waveshare/WM8960-Audio-HAT
  cd WM8960-Audio-HAT
  sudo ./install.sh
  sudo reboot
  ```
