# esp32-serial-led

ESP32 串口控制 LED 作业 — 通过串口发送指令切换 LED 亮灭。

## 硬件接线

| GPIO | 电阻 | LED 正极 | LED 负极 |
|------|------|----------|----------|
| GPIO2 | 220Ω | 长脚 | GND |
| GPIO4 | 220Ω | 长脚 | GND |
| GPIO5 | 220Ω | 长脚 | GND |
| GPIO18 | 220Ω | 长脚 | GND |

## 串口指令

| 指令 | 功能 |
|------|------|
| `1` | 切换 LED1 亮/灭 |
| `2` | 切换 LED2 亮/灭 |
| `3` | 切换 LED3 亮/灭 |
| `4` | 切换 LED4 亮/灭 |
| 其他 | 忽略，打印"未知指令" |

## 即时串口工具

`serial_tool.py` — 按键盘直接发送指令，无需回车（需 `pip install pyserial`）。

```
python serial_tool.py
```

按 1/2/3/4 控制 LED，按 q 退出。

## 使用

- 编译：`pio run`
- 烧录：`pio run -t upload`
- 串口监视器：`pio device monitor`（波特率 115200）
- 在 VSCode 中也可点击底部🔌图标打开串口监视器

## 串口设置

波特率：115200，换行符设为 NL（\n）或 CR+NL
