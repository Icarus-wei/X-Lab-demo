#include <Arduino.h>

// ULN2003 驱动板连接的 ESP32 引脚
const int IN1 = 19;
const int IN2 = 18;
const int IN3 = 5;
const int IN4 = 17;

const int pins[] = {IN1, IN2, IN3, IN4};

// 28BYJ-48 一整圈 = 2048 步
const int STEPS_PER_REV = 4096;

// 步进延时（微秒），改小 = 更快，改大 = 更慢
const int stepDelay = 2000;

// 四相八拍步进序列
const int stepSequence[8][4] = {
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1},
};

void setStep(int step) {
  for (int i = 0; i < 4; i++) {
    digitalWrite(pins[i], stepSequence[step][i]);
  }
}

void rotate(int steps, bool clockwise) {
  static int phase = 0;  // 记住当前相位，连续转动更平滑

  for (int i = 0; i < steps; i++) {
    if (clockwise) {
      phase = (phase + 1) % 8;
    } else {
      phase = (phase + 7) % 8;  // 等价于 (phase - 1 + 8) % 8
    }
    setStep(phase);
    delayMicroseconds(stepDelay);
  }
}

void stopMotor() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(pins[i], LOW);
  }
}

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < 4; i++) {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }

  Serial.println("步进电机就绪");
}

void loop() {
  // 正转一圈
  Serial.println("正转一圈...");
  rotate(STEPS_PER_REV, true);

  // 停顿 1 秒
  stopMotor();
  delay(1000);

  // 反转一圈
  Serial.println("反转一圈...");
  rotate(STEPS_PER_REV, false);

  // 停顿 1 秒
  stopMotor();
  delay(1000);
}
