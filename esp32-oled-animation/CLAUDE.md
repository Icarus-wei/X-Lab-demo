# esp32-oled-animation

ESP32 OLED 动画播放器 — 将视频/图片转为 128×64 单色动画帧，在 OLED 上循环播放。

## 使用的库

U8G2、OpenCV（转换用）、Pillow

## 硬件接线

| OLED | ESP32 |
|------|-------|
| VCC | 3.3V |
| GND | GND |
| SCL | GPIO22 |
| SDA | GPIO21 |

## 转换工具

### 视频转动画（主要）

`video_to_frames.py` — 从视频抽帧、缩放、二值化，生成动画数据。

```bash
pip install opencv-python-headless Pillow
python video_to_frames.py video.mp4 --fps 12 --output src/animation_data.h
```

参数：
- `--fps`：目标帧率（默认取视频原始帧率）
- `--threshold`：二值化阈值 0-255（默认 128）
- `--preview`：同时生成 `animation_data.gif` 预览

### 图片转静态位图

`convert.py` — 单张图片转 XBM 格式。

```bash
pip install Pillow
python convert.py your_image.png
```

## 显示效果

- 动画以设定帧率循环播放
- 数据存储在 flash（PROGMEM），约 1KB/帧

## 使用

- 编译：`pio run`
- 烧录：`pio run -t upload`（需按住 BOOT 进入下载模式）
