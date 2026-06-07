#include <Arduino.h>

// LED 连接的 GPIO 引脚
const int ledPins[] = {2, 4, 5, 18};
const int ledCount = sizeof(ledPins) / sizeof(ledPins[0]);

// 流水灯延时（毫秒），改小 = 更快，改大 = 更慢
const int delayTime = 1000;

void setup() {
  // 将所有 LED 引脚设为输出模式
  for (int i = 0; i < ledCount; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);  // 初始状态熄灭
  }
}

void loop() {
  // 从左到右依次点亮
  for (int i = 0; i < ledCount; i++) {
    digitalWrite(ledPins[i], HIGH);
    delay(delayTime);
    digitalWrite(ledPins[i], LOW);
  }

  // 从右到左依次点亮（回来）
  for (int i = ledCount - 2; i > 0; i--) {
    digitalWrite(ledPins[i], HIGH);
    delay(delayTime);
    digitalWrite(ledPins[i], LOW);
  }
}
