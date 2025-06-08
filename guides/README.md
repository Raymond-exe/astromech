# Astromech Guide

This is a guide for adding audio/video systems to the [BB-R2 3D printed mini droid](https://www.printed-droid.com/kb/bb-r2/) kit from Mr. Baddeley.

**Recommended OS:** *Raspberry Pi OS Lite (64-bit)*  
Linux kernel version: *Linux 6.12.25+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.12.25-1+rpt1 (2025-04-30) aarch64*

You can use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to setup an SD card for this project, just make sure to select your Pi model and the 64-bit Lite OS, or another OS of your prefer.

## Initial Setup

1. **Raspberry Pi OS updates**  
    Start with pulling new packages and upgrading the ones you have:
    ```
    sudo apt update
    sudo apt upgrade
    ```
2. **Install dependencies:**  
    We'll be depending on several packages for front-end stuff, I/O, or version management, you can install separately (using `sudo apt install <package-name>`) or together using this single-line command:
    ```
    sudo apt install git python3-flask python3-picamera2 ffmpeg alsa-utils
    ```

## Setup Guide Pages
This setup guide is split into 3 smaller pages for organization and ease of use:
1. [**HARDWARE & ASSEMBLY GUIDE**](./HARDWARE.md)
2. [**HOTSPOT SETUP**](./HOTSPOT.md)
3. [**SOFTWARE & DRIVER SETUP**](./SOFTWARE.md)

It is recommended you follow each guide in the order listed above, although it's technically possible to go out of order.