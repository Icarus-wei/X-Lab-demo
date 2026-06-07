"""
视频转 OLED 动画帧工具
用法：python video_to_frames.py video.mp4 [--fps 12] [--threshold 128]

输出：src/animation_data.h（自动放到 src/ 目录）
依赖：pip install opencv-python-headless Pillow
"""

import sys
import os
import argparse
import cv2
import numpy as np
from PIL import Image


def extract_frames(video_path, target_fps=None):
    """从视频中抽取帧"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"错误：无法打开视频 {video_path}")
        sys.exit(1)

    src_fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if target_fps is None:
        target_fps = src_fps

    # 计算抽帧间隔
    interval = max(1, round(src_fps / target_fps))
    frames = []
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            frames.append(frame)
        idx += 1

    cap.release()
    print(f"源视频：{src_fps}fps，共 {total} 帧")
    print(f"抽帧间隔：每 {interval} 帧取 1 帧，目标 {target_fps}fps")
    print(f"提取帧数：{len(frames)}")
    return frames


def process_frame(frame, width=128, height=64, threshold=128):
    """将 OpenCV 帧转为 128x64 单色位图"""
    # BGR -> RGB -> PIL
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)

    # 缩放，保持比例居中，黑色填充
    img.thumbnail((width, height), Image.LANCZOS)
    canvas = Image.new("L", (width, height), 0)  # 黑色背景
    offset_x = (width - img.width) // 2
    offset_y = (height - img.height) // 2

    # 转灰度
    gray = img.convert("L")
    canvas.paste(gray, (offset_x, offset_y))

    # 二值化
    pixels = np.array(canvas)
    binary = (pixels >= threshold).astype(np.uint8) * 255
    return binary


def pack_to_xbm_bytes(binary):
    """将 128x64 二值图打包为 XBM 格式字节（每行 16 字节）"""
    h, w = binary.shape
    data = []
    for y in range(h):
        for x_byte in range(w // 8):
            byte_val = 0
            for bit in range(8):
                x = x_byte * 8 + bit
                if binary[y, x] > 0:
                    byte_val |= (1 << bit)
            data.append(byte_val)
    return data


def generate_header(all_frames_data, target_fps, output_path):
    """生成 C 头文件"""
    num_frames = len(all_frames_data)
    frame_size = len(all_frames_data[0])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("// ============================================\n")
        f.write("// 自动生成的动画帧数据\n")
        f.write(f"// 帧数：{num_frames}\n")
        f.write(f"// 帧率：{target_fps}fps\n")
        f.write(f"// 分辨率：128x64\n")
        f.write(f"// 每帧大小：{frame_size} 字节\n")
        f.write(f"// 总大小：{num_frames * frame_size} 字节\n")
        f.write("// ============================================\n\n")
        f.write("#pragma once\n\n")
        f.write("#include <pgmspace.h>\n\n")
        f.write(f"#define ANIM_FRAME_COUNT {num_frames}\n")
        f.write(f"#define ANIM_FPS {target_fps}\n")
        f.write(f"#define ANIM_FRAME_SIZE {frame_size}\n\n")

        # 存储为单个大数组，每帧连续存放
        f.write(f"const uint8_t animation_frames[] PROGMEM = {{\n")
        for i, frame in enumerate(all_frames_data):
            f.write(f"  // Frame {i}\n  ")
            f.write(", ".join(f"0x{b:02X}" for b in frame))
            if i < num_frames - 1:
                f.write(",")
            f.write("\n")
        f.write("};\n")

    print(f"\n输出：{output_path}")
    print(f"总数据量：{num_frames * frame_size} 字节 ({num_frames * frame_size / 1024:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(description="视频转 OLED 动画帧")
    parser.add_argument("video", help="输入视频文件路径")
    parser.add_argument("--fps", type=float, default=None, help="目标帧率（默认与源视频相同）")
    parser.add_argument("--threshold", type=int, default=128, help="二值化阈值 0-255（默认 128）")
    parser.add_argument("--output", default="src/animation_data.h", help="输出头文件路径")
    parser.add_argument("--preview", action="store_true", help="生成预览 GIF")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"错误：文件不存在 {args.video}")
        sys.exit(1)

    # 抽帧
    frames = extract_frames(args.video, args.fps)
    if not frames:
        print("错误：未能提取任何帧")
        sys.exit(1)

    # 处理每一帧
    print(f"\n处理帧...")
    all_data = []
    preview_frames = []
    for i, frame in enumerate(frames):
        binary = process_frame(frame, threshold=args.threshold)
        xbm = pack_to_xbm_bytes(binary)
        all_data.append(xbm)
        if args.preview:
            preview_frames.append(Image.fromarray(binary))
        if (i + 1) % 50 == 0:
            print(f"  已处理 {i + 1}/{len(frames)} 帧")

    print(f"  全部 {len(frames)} 帧处理完成")

    # 生成头文件
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    generate_header(all_data, args.fps or 24, args.output)

    # 生成预览 GIF
    if args.preview and preview_frames:
        gif_path = args.output.replace(".h", ".gif")
        preview_frames[0].save(
            gif_path,
            save_all=True,
            append_images=preview_frames[1:],
            duration=int(1000 / (args.fps or 24)),
            loop=0,
        )
        print(f"预览 GIF：{gif_path}")


if __name__ == "__main__":
    main()
