#include <XBee.h>
#include <Printers.h>
#include <AltSoftSerial.h>

XBeeWithCallbacks xbee = XBeeWithCallbacks();
AltSoftSerial xbeeSerial;

void handleResponse(XBeeResponse& resp, uintptr_t data) {
  Serial.println(F("Handling response"));
  printResponseCb(resp, (uintptr_t)&Serial);
}

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

void loop() {
  xbee.loop();
}
