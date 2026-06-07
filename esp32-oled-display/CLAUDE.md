# esp32-oled-display

ESP32 OLED 显示屏作业 — I2C 驱动 SSD1306 128x64 OLED，显示文字和系统信息。

## 使用的库

**U8G2** — 功能强大的单色图形库，支持多种 OLED/LCD 驱动芯片，内置中文字体。

## 硬件接线

4PIN OLED（I2C）：

| OLED | ESP32 |
|------|-------|
| VCC | 3.3V |
| GND | GND |
| SCL | GPIO22 |
| SDA | GPIO21 |

## 显示内容

画面 1：
- 大号 "Hello!" 标题
- "ESP32 OLED"
- "by 冰糖葫芦"

画面 2（每 2 秒切换）：
- 运行时间
- 可用内存
- CPU 频率

## 使用

- 编译：`pio run`
- 烧录：`pio run -t upload`
- 串口监视器：`pio device monitor`

## 进阶

如需显示图片，可用取模工具将图片转为位图数组，用 `u8g2.drawXBMP()` 显示。
