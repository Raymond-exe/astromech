# Hardware assembly guide

This guide focuses on the physical assembly of the electrical system, wiring between components, and integration into the 3D printed chasis. For the mechanical assembly, refer to Mr. Baddeley's [BB-R2 assembly instructions](https://www.printed-droid.com/wp-content/uploads/2020/09/BB-R2-instructions.pdf).

## Hardware components
| Component | Role | Source | Estimated Current Draw |
| --------- | ---- | ------ | ---------------------- |
| Raspberry Pi Zero 2 W | Main astromech computer | [Amazon](https://www.amazon.com/dp/B09LH5SBPS) | 0.4 - 0.6 A |
| Raspberry Pi Camera Module, wide-angle | Live video feed | [Amazon](https://www.amazon.com/dp/B083XMGSVP) | ~0.25 A |
| WM8960 Audio HAT Module | Audio IO | [Amazon](https://www.amazon.com/dp/B098R7TTM4) | ~0.05 A |
| PCA9685 Servo Driver Board | Servo motor control | [AliExpress](https://www.aliexpress.us/item/3256808620007290.html) | ~0.1 A* |
| 3x MG90S Servo Motors (continuous-rotation) | Main drive wheels, dome rotation | Donated from Rob :) | 0.4 A each (stall) |
| Geekworm X306 UPS Board | Power distribution | [Amazon](https://www.amazon.com/dp/B0B74NT38D) | |
| 18650 Battery Cell (9900mAh) | Power source | [Amazon](https://www.amazon.com/dp/B0CP5N3XMF) | |
| Heatsink case for Raspberry Pi Zero 2 (optional, but recommended)| It's a heatsink.| [Amazon](https://www.amazon.com/dp/B0BLTZKKN9) |
| USB Type-C panel mount adapter | External access to X306 charger port | [Amazon](https://www.amazon.com/dp/B0D93S6C29) |
| USB Type-C 90-degree adapter | | [Amazon](https://www.amazon.com/dp/B0D92JZLW8)
| LED lights | ✨ Aesthetics ✨ | [Amazon](https://www.amazon.com/dp/B01AUI4VSI) |
| Light-up momentary switch | Power Button | [Amazon](https://www.amazon.com/dp/B0DN13M5PF) |

## Assembly instructions

### Main computer stack
1. Screw the heatsink onto (through) the Raspberry Pi, and into the threaded mounting points on the X306 UPS board.
    - *The screws should extend ~2mm past the bottom of the X306 board.*
2. Screw the assembly above into the 3D-printed adapter

## 3D printed parts
Most 3D printed parts are directly from or were modified versions of the parts on [Mr. Baddeley's patreon page](https://www.patreon.com/c/mrbaddeley/home), and are available for purchase as the BB-R2 kit. The dome we used was the "traditional" R2 dome, however any other dome should also work as long as it has the same internal volume as the traditional dome. **All other 3D printed files (body, legs, wheels) are required**.

Since they are available for purchase, only the models which are *not* from Mr. Baddeley's BB-R2 kit, modified or not, are available in the `models/` folder in this repository.



// TODO finish this lol