# esp32-led-flow

ESP32 流水灯作业 — 4 颗 LED 依次点亮，循环往复。

## 硬件接线

| GPIO | 电阻 | LED 正极 | LED 负极 |
|------|------|----------|----------|
| GPIO2 | 220Ω | 长脚 | GND |
| GPIO4 | 220Ω | 长脚 | GND |
| GPIO5 | 220Ω | 长脚 | GND |
| GPIO18 | 220Ω | 长脚 | GND |

## 使用

- 编译：`pio run`
- 烧录：`pio run -t upload`（需插 USB）
- 串口监视器：`pio device monitor`

## 参数调整

修改 `src/main.cpp` 中的 `delayTime` 值可改变流水速度。
