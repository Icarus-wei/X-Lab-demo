#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>

// ESP32 默认 I2C 引脚：SDA=21, SCL=22
// OLED 地址通常为 0x3C，屏幕尺寸 128x64
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(
  U8G2_R0,        // 不旋转
  U8X8_PIN_NONE,  // 不用复位引脚
  22,             // SCL
  21              // SDA
);

void setup() {
  Serial.begin(115200);

  u8g2.begin();
  u8g2.enableUTF8Print();  // 启用 UTF8 支持（中文需要额外字体）

  Serial.println("OLED 初始化完成");
}

void loop() {
  u8g2.clearBuffer();

  // 第一行：大号字体标题
  u8g2.setFont(u8g2_font_logisoso24_tf);
  u8g2.setCursor(0, 30);
  u8g2.print("Hello!");

  // 第二行：小号字体
  u8g2.setFont(u8g2_font_wqy12_t_gb2312);
  u8g2.setCursor(0, 50);
  u8g2.print("ESP32 OLED");

  // 第三行
  u8g2.setCursor(0, 64);
  u8g2.print("by 冰糖葫芦");

  u8g2.sendBuffer();

  delay(2000);

  // --- 画面 2：显示系统信息 ---
  u8g2.clearBuffer();

  u8g2.setFont(u8g2_font_wqy12_t_gb2312);
  u8g2.setCursor(0, 14);
  u8g2.print("== 系统信息 ==");

  u8g2.setCursor(0, 30);
  u8g2.print("运行时间: ");
  u8g2.print(millis() / 1000);
  u8g2.print(" 秒");

  u8g2.setCursor(0, 46);
  u8g2.print("可用内存: ");
  u8g2.print(ESP.getFreeHeap() / 1024);
  u8g2.print(" KB");

  u8g2.setCursor(0, 62);
  u8g2.print("CPU: 240MHz");

  u8g2.sendBuffer();

  delay(2000);
}
