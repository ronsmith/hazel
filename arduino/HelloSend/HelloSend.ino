#include <XBee.h>
#include <Printers.h>
#include <AltSoftSerial.h>

XBeeWithCallbacks xbee = XBeeWithCallbacks();
AltSoftSerial xbeeSerial;

void setup() {
  Serial.begin(9600);
  Serial.println(F("Setup begin"));
  
  xbeeSerial.begin(9600);
  xbee.begin(xbeeSerial);
  Serial.println(F("XBee configured"));
  delay(1);

  Serial.println(F("Sending VR command to XBee"));
  xbee.onResponse(printResponseCb, (uintptr_t)(Print*)&Serial);
  AtCommandRequest req((uint8_t*)"VR");
  xbee.send(req);
  
  Serial.println(F("Setup complete"));
}

void sayHello() {
  ZBTxRequest txRequest;
  txRequest.setAddress64(0x000000000000FFFF);
  char* payload = "Hello XBee!";
  txRequest.setPayload((uint8_t*)payload, strlen(payload));
  uint8_t status = xbee.sendAndWait(txRequest, 5000);
  if (status == 0) {
    Serial.println(F("Succesfully sent packet"));
  } else {
    Serial.print(F("Failed to send packet. Status: 0x"));
    Serial.println(status, HEX);
  }
}

unsigned long lastTxTime = 0;

void loop() {
  xbee.loop();
  if (millis() - lastTxTime > 10000) {
    lastTxTime = millis();
    sayHello();
  }
}
