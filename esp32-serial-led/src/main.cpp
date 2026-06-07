#include <Arduino.h>

// LED 引脚定义
const int ledPins[] = {2, 4, 5, 18};
const int ledCount = sizeof(ledPins) / sizeof(ledPins[0]);

// LED 当前状态（false=灭, true=亮）
bool ledState[] = {false, false, false, false};

// 用于拼接串口接收的字符串
String inputString = "";

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < ledCount; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  Serial.println("ESP32 串口 LED 控制就绪");
  Serial.println("发送 1/2/3/4 切换对应 LED");
}

void toggleLed(int index) {
  if (index < 0 || index >= ledCount) return;  // 无效指令，忽略

  ledState[index] = !ledState[index];
  digitalWrite(ledPins[index], ledState[index] ? HIGH : LOW);

  // 发送反馈
  Serial.print("LED");
  Serial.print(index + 1);
  Serial.println(ledState[index] ? "亮" : "灭");
}

void loop() {
  while (Serial.available() > 0) {
    char inChar = Serial.read();

    if (inChar == '\n' || inChar == '\r') {
      // 收到换行，处理指令
      inputString.trim();

      if (inputString == "1") {
        toggleLed(0);
      } else if (inputString == "2") {
        toggleLed(1);
      } else if (inputString == "3") {
        toggleLed(2);
      } else if (inputString == "4") {
        toggleLed(3);
      } else {
        // 无效指令，不执行动作，但打印提示
        Serial.print("未知指令: ");
        Serial.println(inputString);
      }

      inputString = "";  // 清空，准备接收下一条
    } else {
      inputString += inChar;  // 拼接字符
    }
  }
}
