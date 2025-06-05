#include <unistd.h>
#include <iostream>
#include <cmath>
#include <PiPCA9685/PCA9685.h>

#define NEUTRAL 450
#define PWM_SCALE 400

int pwmFrom(float, int);

int main() {
  PiPCA9685::PCA9685 pca{};

  pca.set_pwm_freq(60.0);

  // for (int angle = 0; angle < 1000; angle++) {
  //   pca.set_pwm(0, 0, angle);
  //   std::cout << angle << "\n";
  //   usleep(25'000);
  // }

  pca.set_pwm(0, 0, NEUTRAL);
}

int pwmFrom(float alpha, int direction) {
  if (direction < -1) direction = -1;
  if (direction > 1) direction = 1;

  if (alpha > 1) alpha = 1;
  if (alpha < 0) alpha = 0;

  return round(alpha * PWM_SCALE * direction) + NEUTRAL;
}
