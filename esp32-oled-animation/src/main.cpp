#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>

// ESP32 默认 I2C 引脚
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(
  U8G2_R0,
  U8X8_PIN_NONE,
  22,  // SCL
  21   // SDA
);

// 动画帧数据
#include "animation_data.h"

void setup() {
  Serial.begin(115200);
  u8g2.begin();
  Serial.printf("动画播放器就绪 - %d 帧, %dfps\n", ANIM_FRAME_COUNT, ANIM_FPS);
}

void loop() {
  static uint32_t lastFrame = 0;
  static uint16_t frameIdx = 0;
  uint32_t interval = 1000 / ANIM_FPS;

  uint32_t now = millis();
  if (now - lastFrame >= interval) {
    lastFrame = now;

    // 从 PROGMEM 读取当前帧数据
    const uint8_t* framePtr = &animation_frames[frameIdx * ANIM_FRAME_SIZE];

    u8g2.clearBuffer();
    u8g2.drawXBMP(0, 0, 128, 64, framePtr);
    u8g2.sendBuffer();

    frameIdx++;
    if (frameIdx >= ANIM_FRAME_COUNT) {
      frameIdx = 0;  // 循环播放
    }
  }
}
