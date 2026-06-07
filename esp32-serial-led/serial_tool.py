"""
串口即时控制工具 — 按键盘直接发送，无需回车
用法：python serial_tool.py
按 1/2/3/4 控制 LED，按 q 退出
"""

import serial
import sys
import msvcrt  # Windows 专用

PORT = "COM6"
BAUD = 115200

def main():
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print(f"已连接 {PORT} @ {BAUD}")
    print("按 1/2/3/4 控制 LED，按 q 退出")
    print("-" * 30)

    try:
        while True:
            # 读取串口输出
            if ser.in_waiting:
                data = ser.read(ser.in_waiting).decode("utf-8", errors="replace")
                print(data, end="", flush=True)

            # 检测键盘输入（无回车）
            if msvcrt.kbhit():
                key = msvcrt.getch().decode("utf-8", errors="replace")
                if key == "q":
                    print("\n退出")
                    break
                if key in ("1", "2", "3", "4"):
                    ser.write((key + "\n").encode())
                    print(f">> 发送: {key}")
                else:
                    print(f"忽略: {key}")

    except KeyboardInterrupt:
        print("\n退出")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
