# esp32-stepper-motor

ESP32 步进电机作业 — 28BYJ-48 + ULN2003，正转一圈 → 停顿 → 反转一圈。

## 硬件接线

ESP32 → ULN2003 驱动板：

| ESP32 | ULN2003 |
|-------|---------|
| GPIO19 | IN1 |
| GPIO18 | IN2 |
| GPIO5 | IN3 |
| GPIO17 | IN4 |
| GND | GND |
| 5V | VCC |

28BYJ-48 电机插头直接插 ULN2003 的电机接口（防反插，插不反）。

## 参数调整

- `stepDelay`：步进延时（微秒），默认 2000μs。改小转速更快，改大转速更慢
- `STEPS_PER_REV`：一圈步数，28BYJ-48 八拍驱动为 4096

## 使用

- 编译：`pio run`
- 烧录：`pio run -t upload`
- 串口监视器：`pio device monitor`
