#include <AltSoftSerial.h>

AltSoftSerial espSerial;

void setup() {
  Serial.begin(9600);
  Serial.println(F("Begin ESP8266Comm sketch"));
  espSerial.begin(2400);
}

char cmd[32];

void loop() {
  while (espSerial.available()) {
    Serial.write(espSerial.read());
  }

  int i = 0;

  while (Serial.available()) {
    cmd[i++] = Serial.read();
    delay(5);
  }

  if (i) {
    cmd[i] = '\0';
    espSerial.println(cmd);
  }
}
