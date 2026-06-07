"""
图片转 XBM 格式工具
用法：python convert.py your_image.png

输出：image_data.h（放到 src/ 目录下）
依赖：pip install Pillow
"""

import sys
from PIL import Image

def convert_to_xbm(input_path, output_path="src/image_data.h", size=(128, 64)):
    img = Image.open(input_path)

    # 转灰度 → 二值化 → 缩放
    img = img.convert("L")
    img = img.point(lambda x: 255 if x > 128 else 0, "1")
    img = img.resize(size, Image.LANCZOS)

    width, height = img.size
    pixels = img.load()

    # 每行需要的字节数（每字存 8 像素）
    bytes_per_row = (width + 7) // 8
    data = []

    for y in range(height):
        for byte_idx in range(bytes_per_row):
            byte_val = 0
            for bit in range(8):
                x = byte_idx * 8 + bit
                if x < width and pixels[x, y] == 0:  # 黑色像素
                    byte_val |= (1 << bit)  # LSB-first
            data.append(byte_val)

    # 生成 C 头文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("// 由 convert.py 自动生成\n")
        f.write(f"// 原图: {input_path}\n")
        f.write(f"// 尺寸: {width}x{height}\n\n")
        f.write(f"#define IMAGE_WIDTH  {width}\n")
        f.write(f"#define IMAGE_HEIGHT {height}\n\n")
        f.write("static const unsigned char image_data[] PROGMEM = {\n  ")

        for i, byte in enumerate(data):
            f.write(f"0x{byte:02X}")
            if i < len(data) - 1:
                f.write(", ")
            if (i + 1) % 16 == 0:
                f.write("\n  ")

        f.write("\n};\n")

    print(f"转换完成: {output_path}")
    print(f"图片尺寸: {width}x{height}")
    print(f"数据大小: {len(data)} 字节")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python convert.py your_image.png")
        print("可选: python convert.py your_image.png 64 32  (自定义宽高)")
        sys.exit(1)

    input_path = sys.argv[1]
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 128
    h = int(sys.argv[3]) if len(sys.argv) > 3 else 64

    convert_to_xbm(input_path, size=(w, h))
