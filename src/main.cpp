#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <cmath>
#include <iostream>
#include <PiPCA9685/PCA9685.h>

#define NEUTRAL 450
#define PWM_SCALE 400

#define FIFO_PIPE "/tmp/servo_ctrl"

int pwmFrom(float, int);

int main() {
    int fifo = open(FIFO_PIPE, O_RDONLY);
    if (fifo == -1) {
        perror("open");
        return 1;
    }

    PiPCA9685::PCA9685 pca{};
    pca.set_pwm_freq(60.0);

    pca.set_pwm(0, 0, NEUTRAL); // channel, on, off

    int channel;
    int direction;
    float speed;

    while (true) {
        if (read(fifo, &channel, sizeof(channel)) > 0 &&
            read(fifo, &direction, sizeof(direction)) > 0 && 
            read(fifo, &speed, sizeof(speed)) > 0
        ) {
            if (channel < 0) {
                break;
            }
            printf("[main.cpp] [ch %d] speed: %f\n", channel, (speed * direction));
            pca.set_pwm(channel, 0, pwmFrom(speed, direction));
        } 
    }

    printf("[main.cpp] Exiting...\n");
    close(fifo);
    return 0;
}

int pwmFrom(float alpha, int direction) {
    if (direction < -1) direction = -1;
    if (direction > 1) direction = 1;

    if (alpha > 1) alpha = 1;
    if (alpha < 0) alpha = 0;

    return round(alpha * PWM_SCALE * direction) + NEUTRAL;
}
