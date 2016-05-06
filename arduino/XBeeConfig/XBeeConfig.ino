#include <SoftwareSerial.h>

SoftwareSerial xbser(8, 9);
String response;

int writeStr(SoftwareSerial& ass, const char* str) {
  int i;
  for (i = 0; str[i]; i++) {
    ass.write(str[i]);
  }
  return i;
}

int writeStr(SoftwareSerial& ass, const __FlashStringHelper* str) {
  return writeStr(ass, (const char *)str);
}

void setup() {
  Serial.begin(9600);
  Serial.println(F("Setup begin"));

  xbser.setTimeout(5000);
  xbser.begin(9600);
  
  Serial.println(F("XBee configuration:"));
  while (1) {
    writeStr(xbser, F("+++"));
    response = xbser.readStringUntil('\r');
    if (response.startsWith(F("OK"))) break;
    Serial.print(F("Error entering command mode. Received \""));
    Serial.print(response);
    Serial.println(F("\" instead of \"OK\".\nWill try again after a short delay."));
    delay(2000);
  }
  writeStr(xbser, F("ATVR\r"));
  response = xbser.readStringUntil('\r');
  Serial.print(F("XBee Firmware Version: "));
  Serial.println(response);
  writeStr(xbser, F("ATSH\r"));
  response = xbser.readStringUntil('\r');
  writeStr(xbser, F("ATSL\r"));
  response += xbser.readStringUntil('\r');
  Serial.print(F("XBee Address: "));
  Serial.println(response);
}

void loop() {
  // put your main code here, to run repeatedly:

}
