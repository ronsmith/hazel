/*******************************************************************************
 * PoolPumController
 * Created By: Ron Smith
 * Copyright ©2016 That Ain't Working, All Rights Reserved
 *******************************************************************************/

#include <limits.h>
#include <TimeLib.h>
#include <XBee.h>
#include <Printers.h>
#include <AltSoftSerial.h>
#include "TemperatureSensor.h"
#include "PumpRelay.h"
#include "TimeBoundary.h"

const int RELAY_PIN     = 2;  // relay coil for pump
const int BUTTON_PIN    = 3;  // button
const int LED_PIN       = 4;  // LED for visual indicator
const int ASSOC_PIN     = 5;  // XBee associate data stream
const int ALT_RX_PIN    = 8;  // used by AltSoftSerial
const int ALT_TX_PIN    = 9;  // used by AltSoftSerial
const int TEMP_PIN      = A0; // variable voltage from temp sensor

XBeeWithCallbacks xbee;
AltSoftSerial xbeeSerial;
TemperatureSensor tempSensor;
PumpRelay pumpRelay;

/*******************************************************************************
 * Use the LED for primitive communication
 *******************************************************************************/
void handleLED() {
  // for now, just pass the value from XBee's associate pin to the LED
  digitalWrite(LED_PIN, digitalRead(ASSOC_PIN));
}


/*******************************************************************************
 * Callback for incoming XBee data
 *******************************************************************************/
void handleXbeeResponse(ZBRxResponse& rx, uintptr_t) {
  Serial.print(F("Received packet from "));
  printHex(Serial, rx.getRemoteAddress64());
  Serial.println();
  Serial.print(F("Payload: "));
  Serial.write(rx.getData(), rx.getDataLength());
  Serial.println();  
}

/*******************************************************************************
 * Setup
 *******************************************************************************/
void setup() {
  Serial.begin(9600);
  Serial.println(F("Setup begin"));

  Serial.println(F("Configuring Temperature Sensor"));
  tempSensor.begin(TEMP_PIN);
  tempSensor.logInterval = 60000; // log temp to Serial every minute
  tempSensor.logTemp();
  
  Serial.print(F("Analog Reference is "));
  Serial.print(tempSensor.mvref/1000.0);
  Serial.println(F("V"));

  Serial.println(F("Configuring Pump Relay"));
  pumpRelay.begin(RELAY_PIN);

  Serial.println(F("Configuring XBee"));
  xbeeSerial.begin(9600);
  xbee.begin(xbeeSerial);
  delay(10);
  xbee.onZBRxResponse(handleXbeeResponse);

  Serial.println(F("Configuring Other Pins"));
  pinMode(BUTTON_PIN,    INPUT);
  pinMode(LED_PIN,      OUTPUT);
  digitalWrite(LED_PIN,  LOW);
  pinMode(ASSOC_PIN,    INPUT);

  Serial.println(F("Setup complete"));
}


/*******************************************************************************
 * Main Loop
 *******************************************************************************/
void loop() {
  xbee.loop();
  tempSensor.loop();
  pumpRelay.loop(tempSensor.celcius(), (digitalRead(BUTTON_PIN) == HIGH));
  handleLED();
}
